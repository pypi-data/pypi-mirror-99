from typing import Callable, List, Union

from .authentication import Authentication
from .entity import Entity
from .service import Service


class Pipeline:
    """
    Class to execute multiple services on after the other
    """

    def __init__(self, services: List[Service]):
        """
        Init a Pipeline with the services to execute

        Args:
            services (List[Service]): list of the services to execute. This first service of
                the list is the first service executed.
        """
        for service in services:
            assert isinstance(service, Service)
        self.services = services

    @classmethod
    def from_entities(
        cls,
        entities: List[Entity],
        auth_object: str = None,
        auth_file: str = None,
        scope: str = None,
        use_cache: bool = True,
        cache_dir="~/.cache/elg",
    ):
        """
        Class method to init a Pipeline using a list of entities which will be convert into services
        using the `from_entity` class method of the Service class. Refer to this method for further explanation.
        """
        return cls(
            [
                Service.from_entity(
                    entity=entity,
                    auth_object=auth_object,
                    auth_file=auth_file,
                    scope=scope,
                    use_cache=use_cache,
                    cache_dir=cache_dir,
                )
                for entity in entities
            ]
        )

    @classmethod
    def from_ids(
        cls,
        ids: List[int],
        auth_object: Authentication = None,
        auth_file: str = None,
        scope: str = None,
        domain: str = None,
        use_cache: bool = True,
        cache_dir: str = "~/.cache/elg",
    ):
        """
        Class method to init a Pipeline using a list of ids which will be convert into services
        using the `from_id` class method of the Service class. Refer to this method for further explanation.
        """
        return cls(
            [
                Service.from_id(
                    id=id,
                    auth_object=auth_object,
                    auth_file=auth_file,
                    scope=scope,
                    domain=domain,
                    use_cache=use_cache,
                    cache_dir=cache_dir,
                )
                for id in ids
            ]
        )

    def __call__(
        self,
        input_str: str,
        sync_mode: bool = False,
        timeout: int = None,
        check_file: bool = True,
        verbose: bool = True,
        output_funcs: Union[str, Callable, List[Union[str, Callable]]] = "auto",
    ):
        if isinstance(output_funcs, str) and output_funcs != "auto":
            raise ValueError(
                "output_funcs must be set to 'auto', a callable object, or a list of 'auto' or callable objects with the same length as the number of services in self.services."
            )
        elif isinstance(output_funcs, str) or isinstance(output_funcs, Callable):
            output_funcs = [output_funcs for _ in range(len(self.services))]
        elif isinstance(output_funcs, List):
            if len(output_funcs) != len(self.services):
                raise ValueError(
                    "output_funcs must be set to 'auto', a callable object, or a list of 'auto' or callable objects with the same length as the number of services in self.services."
                )
            for output_func in output_funcs:
                if not ((isinstance(output_func, str) and output_func == "auto") or isinstance(output_func, Callable)):
                    raise ValueError(
                        "output_funcs must be set to 'auto', a callable object, or a list of 'auto' or callable objects with the same length as the number of services in self.services."
                    )
        else:
            raise ValueError(
                "output_funcs must be set to 'auto', a callable object, or a list of 'auto' or callable objects with the same length as the number of services in self.services."
            )

        result = input_str
        results = []
        for service, output_func in zip(self.services, output_funcs):
            result = service(
                input_str=result,
                sync_mode=sync_mode,
                timeout=timeout,
                check_file=check_file,
                verbose=verbose,
                output_func=output_func,
            )
            results.append(result)
            if verbose:
                print(f"Result:\n\t{result}\n")
        return results
