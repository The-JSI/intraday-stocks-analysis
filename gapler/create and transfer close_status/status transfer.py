#transfer the close_status column from close status create.py to the required datasets
import pandas as pd

def transfer_status(source_file, target_files, output_suffix="_with_status"):
    # Load the source file
    source_df = pd.read_excel(source_file)

    # Standardize column names
    source_df.columns = source_df.columns.str.strip().str.lower()

    if "close_status" not in source_df.columns:
        raise ValueError("Source file must have a 'close_status' column")

    # Ensure date is datetime without time
    source_df["date"] = pd.to_datetime(source_df["date"]).dt.date

    # Create merge key
    source_df["merge_key"] = source_df["date"].astype(str) + "_" + source_df["symbol"].astype(str)

    for target_file in target_files:
        target_df = pd.read_excel(target_file)
        target_df.columns = target_df.columns.str.strip().str.lower()

        # Ensure datetime (date only)
        target_df["date"] = pd.to_datetime(target_df["date"]).dt.date

        # Create merge key
        target_df["merge_key"] = target_df["date"].astype(str) + "_" + target_df["symbol"].astype(str)

        # Merge
        merged_df = pd.merge(
            target_df,
            source_df[["merge_key", "close_status"]],
            on="merge_key",
            how="left"
        )

        # Drop helper column
        merged_df.drop(columns=["merge_key"], inplace=True)

        # Save (dates will be clean YYYY-MM-DD)
        output_file = target_file.replace(".xlsx", f"{output_suffix}.xlsx")
        merged_df.to_excel(output_file, index=False)

        # Print summary
        total = len(target_df)
        matched = merged_df["close_status"].notna().sum()
        print(f"{target_file} → {output_file}: {matched}/{total} rows matched with close_status.")

if __name__ == "__main__":
    source = "fut 5 with status complete.xlsx"
    targets = ["gapler 3.xlsx", "gapler 3 5% intraday.xlsx"]
    transfer_status(source, targets)
