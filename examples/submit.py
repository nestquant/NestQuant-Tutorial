import os
import sys
import time
sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from src.submit import Submission

def print_dash_line(n: int=50):
    print(''.join(['-']*n))

if __name__ == "__main__":
    s = Submission(tournament_search_id='return_and_risk_tournament', api_key=os.getenv('API_KEY'))

    # Test data
    symbol = 'BTC'
    model_id = 'test_model_id'
    cur_time = int(time.time())*1000

    # Round down OPEN_TIME to round time (00:00 or 12:00 UTC)
    backtest_example_data = [{"OPEN_TIME": cur_time - cur_time%(12*3600000) - 12*100*3600000, "PREDICTION": 0.487618394396533}]
    
    # Submission for back_test mode
    print_dash_line()
    submission_time = s.submit(is_backtest=True, data=backtest_example_data, symbol=symbol, model_id=model_id)
    print("Example submission - Submission time:", submission_time)

    # Get all submissions
    print_dash_line()
    print("All backtest submissions:", s.get_submission_times(is_backtest=True, symbol=symbol))

    # Waiting for results
    time.sleep(5)

    # Get all submissions
    print_dash_line()
    print("Get result:", s.get_result(is_backtest=True, symbol=symbol, model_id=model_id, submission_time=submission_time))

    # Delete one submission
    print_dash_line()
    print(s.delete_back_test_submission_times(symbol=symbol, model_id=model_id, submission_time=submission_time))

    # Get current round
    print_dash_line()
    print(s.get_current_round_time())


