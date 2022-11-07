import argparse
from datetime import datetime

#parse the inputs(start_date end_date output)
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-date', type = str)
    parser.add_argument('--end-date', type = str)
    parser.add_argument('--output', type = str)
    args = parser.parse_args()
    args.start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    args.end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
    return args