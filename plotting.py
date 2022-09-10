import pandas as pd
import matplotlib.pyplot as plt
import argparse
import scipy
import numpy as np

START_DATE = pd.Timestamp("2017-09-05")
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


def crop_bench_data(benches):
    cond = (START_DATE <= benches["Datum"]) & (benches["Datum"] <= END_DATE)
    resulting_benches = benches[cond]
    return resulting_benches


def draw_side_by_side_plots(benches, temperature):
    _fig, axes = plt.subplots(1, 2)
    # Draw the two plots next to each other 
    t_axis = axes[0]
    b_axis = axes[1]

    t_axis.set_xlabel("Datum")
    t_axis.set_ylabel("Průměrná teplota ve stupních Celsia")

    b_axis.set_xlabel("Datum")
    b_axis.set_ylabel("Počet minut nabíjení")

    benches.plot(x="Datum", y="Nabijeni", kind="line", ax=b_axis)
    temperature.plot(x="date", y="T-AVG", ax=t_axis, color="red")
    plt.show()


def visualize_regression_results(x, y, reg_results):
    print("=== Regression results ===")
    print(f"regression results: {reg_results}")
    regressed_values = x.copy()
    assert regressed_values.shape == x.shape
    regressed_values = regressed_values * reg_results.slope + reg_results.intercept
    _fig, axis = plt.subplots(1, 1)

    axis.set_xlabel("Průměrná teplota ve stupních Celsia")
    axis.set_ylabel("Počet minut nabíjení")
    
    axis.scatter(x, y)
    axis.plot(x, regressed_values)
    plt.show()


def split_days_of_week(benches):
    weekend = []
    weekday = []
    for date in benches["Datum"]:
        weekend.append(date.isoweekday() > 5)
        weekday.append(date.isoweekday() <= 5)
    return benches["Nabijeni"][weekend], benches["Nabijeni"][weekday]


# test whether the 
def ttest(weekends, weekdays):
    print("=== T-test results for weekdays and weekends ===")
    print(scipy.stats.ttest_ind(weekends, weekdays))

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Example plotter for the statistical task")
    parser.add_argument("--temperature-csv", type=str, required=True, help="The CSV filename to read temperatures from")
    parser.add_argument("--bench-csv", type=str, required=True, help="The CSV filename to read bench data from")
    args = parser.parse_args()

    temperature = pd.read_csv(args.temperature_csv)
    temperature = add_datetime(temperature)
    benches = pd.read_csv(args.bench_csv)

    benches["Datum"] = pd.to_datetime(benches["Datum"])
    benches = crop_bench_data(benches)
    
    # draw an overview
    draw_side_by_side_plots(benches, temperature)

    # try linear regression to test correlation
    regression_results = scipy.stats.linregress(temperature["T-AVG"], y=benches["Nabijeni"])
    # print the results and draw a plot
    visualize_regression_results(temperature["T-AVG"], benches["Nabijeni"], regression_results)

    weekends, weekdays = split_days_of_week(benches)
    ttest(weekends, weekdays)

