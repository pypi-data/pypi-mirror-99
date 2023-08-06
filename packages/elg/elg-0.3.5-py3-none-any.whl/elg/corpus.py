from pathlib import Path
from typing import List

import requests
from tqdm import tqdm

from .entity import Entity
from .utils import (CORPUS_DOWNLOAD_URL, LICENCE_URL, get_domain, get_en_value,
                    get_information, get_metadatarecord,
                    map_metadatarecord_to_result)
from .utils.errors import (NotCorpusException, catch_requests_error,
                           ensure_response_ok)


class Licence:
    """
    Class to represent a licence
    """

    def __init__(
        self,
        name: str,
        urls: List[str],
        identifiers: List[dict],
    ):
        self.name = name
        self.urls = urls
        self.identifiers = identifiers

    @classmethod
    def from_data(cls, data: dict):
        name = get_en_value(get_information(id=-1, obj=data, infos="licence_terms_name"))
        urls = get_information(id=-1, obj=data, infos="licence_terms_url")
        identifiers = get_information(id=-1, obj=data, infos="licence_identifier")
        return cls(
            name=name,
            urls=urls,
            identifiers=identifiers,
        )

    def _get_elg_licence_identifier(self):
        for identifier in self.identifiers:
            if identifier["licence_identifier_scheme"] == "http://w3id.org/meta-share/meta-share/elg":
                return identifier["value"]
        return None


class Distribution:
    """
    Class to represent a corpus distribution
    """

    def __init__(
        self,
        corpus_id: int,
        domain: str,
        form: str,
        distribution_location: str,
        download_location: str,
        access_location: str,
        licence: Licence,
        cost: str,
        attribution_text: str,
    ):
        self.corpus_id = corpus_id
        self.domain = domain
        self.form = form
        self.distribution_location = distribution_location
        self.download_location = download_location
        self.access_location = access_location
        self.licence = licence
        self.cost = cost
        self.attribution_text = attribution_text

    @classmethod
    def from_data(cls, corpus_id: int, domain: str, data: dict):
        """
        Class method to init the distribution object from the metadata information.

        Args:
            corpus_id (int): id of the corpus the distribution is from.
            domain (str): ELG domain you want to use. "live" to use the public ELG, "dev" to use the development ELG and
                another value to use a local ELG.
            data (dict): metadata information of the distribution.

        Returns:
            elg.Distribution: the distribution object initialized.
        """
        form = get_information(id=-1, obj=data, infos="dataset_distribution_form")
        distribution_location = get_information(id=-1, obj=data, infos="distribution_location", none=True)
        download_location = get_information(id=-1, obj=data, infos="download_location", none=True)
        access_location = get_information(id=-1, obj=data, infos="access_location", none=True)
        licence_terms = get_information(id=-1, obj=data, infos="licence_terms")
        assert isinstance(licence_terms, list) and len(licence_terms) == 1, licence_terms
        licence = Licence.from_data(licence_terms[0])
        cost = get_information(id=-1, obj=data, infos="cost", none=True)
        if cost is not None:
            cost = "{} {}".format(
                get_information(id=-1, obj=cost, infos="amount"),
                get_information(id=-1, obj=cost, infos="currency").split("/")[-1],
            )
        attribution_text = get_information(id=-1, obj=data, infos="attribution_text", none=True)
        if attribution_text is not None:
            attribution_text = get_en_value(attribution_text)
        return cls(
            corpus_id=corpus_id,
            domain=domain,
            form=form,
            distribution_location=distribution_location,
            download_location=download_location,
            access_location=access_location,
            licence=licence,
            cost=cost,
            attribution_text=attribution_text,
        )

    def is_downloadable(self) -> str:
        """
        Method to get if the distribution is downloadable.

        Returns:
            bool: return True is the distribution is downloadable, False if not.
        """
        if self.form == "http://w3id.org/meta-share/meta-share/downloadable":
            return True
        return False

    @catch_requests_error
    def get_download_url(self) -> str:
        """
        Method to obtain the download url of the distribution if it exists.

        Returns:
            str: url to download the dataset if it exists, else None.
        """
        if self.access_location is not None and self.access_location != "":
            not_downloadable = f"This corpus distribution is not downloadable from the ELG. The corpus is accessible by clicking: {self.access_location}"
        elif self.distribution_location is not None and self.distribution_location != "":
            not_downloadable = f"This corpus distribution is not downloadable from the ELG. The corpus is distributed at the following URL: {self.distribution_location}"
        else:
            not_downloadable = "This corpus distribution is not downloadable from the ELG."
        if not self.is_downloadable():
            print(not_downloadable)
            return None
        if self.download_location is not None and self.download_location != "":
            return self.download_location
        elg_licence_identifier = self.licence._get_elg_licence_identifier()
        if elg_licence_identifier is not None:
            elg_licence_url = LICENCE_URL.format(domain=self.domain, licence=elg_licence_identifier)
            # check if the elg_licence_url exists
            response = requests.get(elg_licence_url)
            if not response.ok:
                print(not_downloadable)
                return None
            print(f"Please, visit the licence of this corpus distribution by clicking: {elg_licence_url}\n")
            accept = input("Do you accept the licence terms: (yes/[no]): ")
            if accept not in ["yes", "Yes", "y", "Y"]:
                print("You need to accept the licence terms to download this corpus distribution.")
                return None
        data = {"licences": [f"{elg_licence_identifier}"]}
        response = requests.post(CORPUS_DOWNLOAD_URL.format(domain=self.domain, id=self.corpus_id), json=data)
        if response.ok:
            return response.json()["s3-url"]
        print(not_downloadable)
        return None

    @catch_requests_error
    def download(self, filename: str = None, folder: str = "./"):
        """Method to download the distribution if possible.

        Args:
            filename (str, optional): Name of the output file. If None, the name of the downloaded file will be used.
                Defaults to None.
            folder (str, optional): path to the folder where to save the downloaded file. Defaults to "./".
        """
        url = self.get_download_url()
        if url is None:
            return None
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        if isinstance(filename, str):
            # use the given filename with the correct extension
            extension = url.split("?")[0].split(".")[-1]
            filename = folder / Path(filename + ("." + extension if len(extension) <= 5 else ""))
        else:
            # use the filename of the file to download
            filename = folder / Path(url.split("?")[0].split("/")[-1])
        print(f"\nDownloading the corpus distribution to {filename}:")
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        with open(filename, "wb") as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        ensure_response_ok(response)
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("Something went wrong during the downloading. The file may be not usable.")


class Corpus(Entity):
    """
    Class to represent a corpus
    """

    def __init__(
        self,
        id: int,
        resource_name: str,
        resource_short_name: List[str],
        resource_type: str,
        entity_type: str,
        description: str,
        keywords: List[str],
        detail: str,
        licences: List[str],
        languages: List[str],
        country_of_registration: List[str],
        creation_date: str,
        last_date_updated: str,
        functional_service: bool,
        functions: List[str],
        intended_applications: List[str],
        views: int,
        downloads: int,
        size: int,
        service_execution_count: int,
        status: str,
        under_construction: bool,
        record: dict,
        domain: str,
    ):
        """
        Init a Corpus object with the corpus information
        """

        super().__init__(
            id=id,
            resource_name=resource_name,
            resource_short_name=resource_short_name,
            resource_type=resource_type,
            entity_type=entity_type,
            description=description,
            keywords=keywords,
            detail=detail,
            licences=licences,
            languages=languages,
            country_of_registration=country_of_registration,
            creation_date=creation_date,
            last_date_updated=last_date_updated,
            functional_service=functional_service,
            functions=functions,
            intended_applications=intended_applications,
            views=views,
            downloads=downloads,
            size=size,
            service_execution_count=service_execution_count,
            status=status,
            under_construction=under_construction,
            domain=domain,
            record=record,
        )
        if self.resource_type != "Corpus":
            raise NotCorpusException(self.id)
        self.distributions = [
            Distribution.from_data(self.id, self.domain, data)
            for data in get_information(
                id=id, obj=self.record, infos=["described_entity", "lr_subclass", "dataset_distribution"]
            )
        ]

    @classmethod
    def from_id(
        cls,
        id: int,
        domain: str = "live",
        use_cache: bool = True,
        cache_dir: str = "~/.cache/elg",
    ):
        """
        Class method to init a corpus from its id.

        Args:
            id (int): id of the corpus.
            domain (str, optional): ELG domain you want to use. "live" to use the public ELG, "dev" to use the
                development ELG and another value to use a local ELG. Defaults to "live".
            use_cache (bool, optional): True if you want to use cached files. Defaults to True.
            cache_dir (str, optional): path to the cache_dir. Set it to None to not store any cached files. Defaults to "~/.cache/elg".

        Returns:
            elg.Corpus: the corpus object initialized.
        """
        domain = get_domain(domain)
        record = get_metadatarecord(id=id, domain=domain, use_cache=use_cache, cache_dir=cache_dir)
        result = map_metadatarecord_to_result(id, record)
        result["domain"] = domain
        return cls(**result)

    @classmethod
    def from_entity(cls, entity):
        if entity.record is None:
            entity.record = get_metadatarecord(
                id=entity.id, domain=entity.domain, use_cache=use_cache, cache_dir=cache_dir
            )
        parameters = entity.__dict__
        return cls(**parameters)

    def download(self, distribution_idx: int = 0, filename: str = None, folder: str = "./"):
        """
        Method to download the corpus if possible.

        Args:
            distribution_idx (int, optional): Index of the distribution of the corpus to download. Defaults to 0.
            filename (str, optional): Name of the output file. If None, the name of the corpus will be used. Defaults to None.
            folder (str, optional): path to the folder where to save the downloaded file. Defaults to "./".
        """
        print(f"Downloading:\n\t[{self.id}] {self.resource_name}\n")
        filename = (
            filename
            if filename is not None
            else "_".join(
                [w for w in "".join(c if c.isalnum() else " " for c in self.resource_name).split(" ") if w != ""]
            )
        )
        self.distributions[distribution_idx].download(
            filename=filename,
            folder=folder,
        )
