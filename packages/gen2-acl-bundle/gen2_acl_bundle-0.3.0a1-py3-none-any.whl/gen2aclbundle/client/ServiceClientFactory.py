from azure.storage.filedatalake import DataLakeServiceClient


class ServiceClientFactory:
    def __init__(self, storage_account_name: str, storage_account_key: str):
        self.__storage_account_name = storage_account_name
        self.__storage_account_key = storage_account_key

    def create(self):
        return DataLakeServiceClient(
            account_url="{}://{}.dfs.core.windows.net".format("https", self.__storage_account_name), credential=self.__storage_account_key
        )
