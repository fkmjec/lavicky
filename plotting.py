import pandas as pd
import matplotlib.pyplot as plt
import argparse
import scipy

START_DATE = pd.Timestamp("2017-07-01")
END_DATE = pd.Timestamp("2018-01-31")


def add_datetime(dataframe):
    result = []
    years = dataframe["rok"]
    months = dataframe["mesic"]
    days = dataframe["den"]
    # warning - this is not robust at all
    for i, (year, month, day) in enumerate(zip(years, months, days)):
        date = pd.Timestamp(f"{year}-{month}-{day}")
        result.append(date)
    dataframe["date"] = result
    cond = (START_DATE <= dataframe["date"]) & (dataframe["date"] <= END_DATE)
    resulting_dataframe = dataframe[cond]
    return resulting_dataframe


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Example plotter for the statistical task")
    parser.add_argument("--temperature-csv", type=str, required=True, help="The CSV filename to read temperatures from")
    parser.add_argument("--bench-csv", type=str, required=True, help="The CSV filename to read bench data from")
    args = parser.parse_args()

    temperature = pd.read_csv(args.temperature_csv)
    cropped_dates = add_datetime(temperature)
    benches = pd.read_csv(args.bench_csv)
    # ax = plt.gca()

    benches["Datum"] = pd.to_datetime(benches["Datum"])
    fig, axes = plt.subplots(1, 2)
    t_axis = axes[0]
    b_axis = axes[1]

    t_axis.set_xlabel("Datum")
    t_axis.set_ylabel("Průměrná teplota ve stupních Celsia")

    b_axis.set_xlabel("Datum")
    b_axis.set_ylabel("Počet minut nabíjení")

    benches.plot(x="Datum", y="Nabijeni", kind="line", ax=b_axis)
    cropped_dates.plot(x="date", y="T-AVG", ax=t_axis, color="red")

    

    plt.show()