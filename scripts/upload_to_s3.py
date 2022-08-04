import pandas as pd
from tqdm import tqdm

tqdm.pandas()

REPORTS_DATA = "s3://ufo.camera/nuforc_reports.csv"
PROCESSED_DATA = "data/processed/nuforc_reports.csv"


def upload_csv_to_s3():
    """Upload csv to s3"""
    print("="*100)
    print("Uploading CSV to s3")
    print("="*100)
    df = pd.read_csv(PROCESSED_DATA)
    df.to_csv(REPORTS_DATA)
    print("Done!")


if __name__ == "__main__":
    upload_csv_to_s3()
