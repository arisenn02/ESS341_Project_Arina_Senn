import matplotlib.pyplot as plt
import mapclassify
def plot_category_over_years(data,categories,time_column,category_column):
    data = data.set_index(time_column)
    fig, ax = plt.subplots()
    colors=["steelblue","seagreen","sandybrown","mediumpurple","lightcoral","cadetblue","rosybrown","darkseagreen","tan","plum"]
    i=0
    for cat in categories:
        filtered_data = data[data[category_column]==cat]
        monthly_reports = filtered_data.resample("ME").size().reset_index(name="reports")
        ax.plot(monthly_reports[time_column], monthly_reports["reports"],color=colors[i],label = cat,)
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

def calculate_mean_processing_time(data,category,category_col="Category",report_col="Report_time",
                                   resolved_col="Resolved_time",boundary_col="Neighborhoods"):
    filter_category = data[data[category_col] == category].copy()
    filter_category["processing_time"] = (filter_category[resolved_col] - filter_category[report_col])
    mean_days = (filter_category.groupby(boundary_col)["processing_time"].mean().reset_index())
    mean_days["processing_time_days"] = (mean_days["processing_time"].dt.total_seconds() / 86400)
    return mean_days

def clean_legend_labels(ax):
    legend = ax.get_legend()
    for text in legend.get_texts():
        text.set_text(text.get_text().replace(",", "  -"))

def add_labels_zurich(ax, data, column_boundary="Neighborhoods", column_geometry="Geometry", names=None):
    selected_quartiere =data[data["Neighborhoods"].isin(names)]
    for i in range(len(selected_quartiere)):
        x = selected_quartiere.iloc[i][column_geometry].centroid.x
        y = selected_quartiere.iloc[i][column_geometry].centroid.y
        name = selected_quartiere.iloc[i][column_boundary]
        
        ax.text(x, y, name, fontsize=7, fontweight="light")

def histogram_natural_breaks(data, column,k):
    classifier = mapclassify.NaturalBreaks(data[column],k=k)
    breaks = classifier.bins
    
    plt.figure(figsize=(10,5))
    plt.hist(data[column], bins=100, color= "grey",edgecolor="black")
    
    for i in breaks:
        plt.axvline(i, color="red", linestyle="--")

    plt.title(f"Distribution of {column} with Natural Breaks")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.show()
