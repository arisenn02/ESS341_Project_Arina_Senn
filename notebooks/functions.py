import matplotlib.pyplot as plt
def plot_category_over_years(data,categories,time_column,category_column):
    data = data.set_index(time_column)
    fig, ax = plt.subplots()
    colors=["steelblue","seagreen","sandybrown","mediumpurple","lightcoral","cadetblue","rosybrown","darkseagreen","tan","plum"]
    i=0
    for cat in categories:
        filtered_data = data[data[category_column]==cat]
        monthly_reports = filtered_data.resample("ME").size().reset_index(name="reports")
        ax.plot(monthly_reports[time_column], monthly_reports["reports"],color=colors[i],label = category,)
        i+=1
    ax.set_xlabel("Time [Year]")
    ax.set_ylabel("Number of Reports")
    ax.set_title("Monthly Reports by Category over Years")
    ax.legend()
    plt.show()


def plot_category_over_a_year(data,categories,time_column, category_column,year):
    data = data.set_index(time_column)
    fig, ax = plt.subplots()
    colors=["steelblue","seagreen","sandybrown","mediumpurple","lightcoral","cadetblue","rosybrown","darkseagreen","tan","plum"]
    i=0
    for cat in categories:
        filtered_data = data[data[category_column]==cat]
        report_year = filtered_data[filtered_data.index.year == year]
        monthly_reports = report_year.resample("ME").size().reset_index(name="reports")
        ax.plot(monthly_reports[time_column], monthly_reports["reports"],"o-",color=colors[i],label=cat,)
        i+=1
    ax.set_xlabel("Time [Month]")
    ax.set_ylabel("Number of Reports")
    ax.set_title("Monthly Reports by Category over a Year")
    ax.legend(loc="upper left",)
    plt.show()

def calculate_mean_processing_time(data,categories):
    for category in categories:
        filter_category= data[data["category"]==category]
        filter_category["processing_time"] =  filter_category["resolved_time"]- filter_category["report_time"]
        mean = (filter_category.groupby(["Quartier"])["processing_time"].mean().reset_index())
        mean["processing_time_float"]= mean["processing_time"].dt.total_seconds()/86400
        
    return mean
        
