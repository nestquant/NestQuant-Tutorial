from typing import List

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from src.base import Base

class Submission(Base):
    def __init__(self, api_key, tournament_search_id: str):
        super().__init__(api_key=api_key)
        self._tournament_search_id = tournament_search_id
        self._cur_round_url = Submission.NESTQUANT_API_ENDPOINT + f'tournament/{tournament_search_id}/current-round'
        self._submission_times_url = Submission.NESTQUANT_API_ENDPOINT + f'tournament/{tournament_search_id}/submission-time/all?api_key=' + self._api_key
        self._result_url = Submission.NESTQUANT_API_ENDPOINT + f'tournament/{tournament_search_id}/submission/overall-performance?api_key=' + self._api_key
        self._submit_url = Submission.NESTQUANT_API_ENDPOINT + f'tournament/{tournament_search_id}/submit/api?api_key=' + self._api_key
        self._delete_submission_url = Submission.NESTQUANT_API_ENDPOINT + f'tournament/{tournament_search_id}/submission?api_key=' + self._api_key
        
    def __convert_dict_to_url_str(
        self,
        d: List[dict]
    ) -> str:
        """
            Convert list of dictionary to string - this is a helper function for submit method

            Parameters
            -----------
                d: List[dict],
                    data in list of dictionary format

            Returns
            ----------
                data in string format
        """
        return str(d).replace("'", '"')

    def submit(
        self,
        is_backtest: bool,
        data: List[dict],
        symbol: str,
        model_id: str
    ) -> int:
        """
            Submit model's output

            Parameters
            -----------
                is_backtest: bool,
                    whether we choose to submit for backtesting or not
                data: List[dict],
                    data in list of dictionary format
                symbol: str,
                    provided symbol, exclusively utilized for the purpose of backtesting
                model_id: str,
                    provided model id

            Returns
            ----------
                submission_time: int
                    recorded submission time
        """
        if is_backtest:
            res = self._post(self._submit_url + f'&submission_type=back_test&symbol={symbol}&model_id={model_id}', data=self.__convert_dict_to_url_str(data))
        else:
            res = self._post(self._submit_url + f'&submission_type=live&symbol={symbol}&model_id={model_id}', data=self.__convert_dict_to_url_str(data))
        submission_time = res.json()['Submission time']
        return submission_time

    def get_submission_times(
        self,
        is_backtest: bool, 
        symbol: str=None
    ) -> dict:
        """
            Get all the recorded submission times

            Parameters
            -----------
                is_backtest: bool,
                    whether we choose to submit for backtesting or not
                symbol: str, default None,
                    provided symbol, exclusively utilized for the purpose of backtesting

            Returns
            ----------
                res: dict
                    all recorded submission time
        """
        if is_backtest:
            res = self._get(self._submission_times_url + f'&submission_type=back_test&symbol={symbol}')
        else:
            res = self._get(self._submission_times_url + f'&submission_type=live&symbol={symbol}')
        return res.json()
    
    def delete_back_test_submission_times(
        self,
        symbol: str,
        model_id: str,
        submission_time: int
    ) -> dict:
        """
            Delete one submission (backtest only)

            Parameters
            -----------
                symbol: str, default None,
                    provided symbol, exclusively utilized for the purpose of backtesting
                model_id: str,
                    ID of the model
                submission_time: int,
                    recorded submission time

            Returns
            ----------
                res: dict
                    all deleted submission time
        """
        res = self._delete(self._delete_submission_url + f'&submission_type=back_test&symbol={symbol}&model_id={model_id}&submission_time={submission_time}')
        return res.json()

    def get_result(
        self,
        is_backtest: bool, 
        submission_time: int,
        symbol: str,
        model_id: str
    ) -> dict:
        """
            Get model's performance

            Parameters
            -----------
                is_backtest: bool,
                    whether we choose to submit for backtesting or not
                submission_time: int,
                    recorded submission time
                symbol: str, default None,
                    provided symbol, exclusively utilized for the purpose of backtesting
                model_id: str,
                    provided model id

            Returns
            ----------
                res: dict
                    all scores of the model
        """
        if is_backtest:
            res = self._get(self._result_url + f'&submission_type=back_test&symbol={symbol}&model_id={model_id}&submission_time={submission_time}')
        else:
            res = self._get(self._result_url + f'&submission_type=live&symbol={symbol}&model_id={model_id}&submission_time={submission_time}')
        return res.json()

    def get_current_round_time(self):
        return self._get(self._cur_round_url).json()
