from __future__ import absolute_import

from aoa.api.iterator_base_api import IteratorBaseApi


class TrainedModelEventApi(IteratorBaseApi):

    path = "/api/trainedModelEvents/"

    def find_all(self, projection: str = None, page: int = None, size: int = None, sort: str = None):
        """
        returns all trained model events

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all trained model events
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id, 
            self.aoa_client.select_header_accept([
                'application/json', 
                'application/hal+json', 
                'text/uri-list', 
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection', 'page', 'sort', 'size', 'sort']
        query_vals = [projection, page, sort, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path,
            header_params,
            query_params)

    def find_by_id(self, event_id: str, projection: str = None):
        """
        returns a trained model event

        Parameters:
           event_id (str): job id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): trained model event
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + event_id,
            header_params,
            query_params)

    def find_by_status(self, status: str, projection: str = None, page: int = None, size: int = None,
                       sort: str = None):
        """
        returns trained model events by status

        Parameters:
           status (str): status of trained model event
            Available values : TRAINED, EVALUATED, APPROVED, REJECTED, CHAMPION, DEPLOYED, RETIRED
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): trained model events
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['status', 'projection', 'page', 'sort', 'size', 'sort']
        query_vals = [status, projection, page, sort, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + 'search/findByStatus',
            header_params,
            query_params)

    def find_by_trained_model_id(self, trained_model_id: str, projection: str = None,
                                 page: int = None, size: int = None, sort: str = None):
        """
        returns trained model events by trained model id

        Parameters:
           trained_model_id (str): trained model id(uuid)
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): trained model events
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['trainedModelId', 'projection', 'page', 'sort', 'size', 'sort']
        query_vals = [trained_model_id, projection, page, sort, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + 'search/findByTrainedModelId',
            header_params,
            query_params)
