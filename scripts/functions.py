import matplotlib.pyplot as plt
import mapclassify

def plot_category_over_years(
    data,
    categories,
    time_column = "Report_time", 
    category_column="Category"):
    """ 
    Plot the monthly number of reports for multiple categories over time.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing report times and category information

    categories : list
        List of categories to include in the plot.

    time_column: datetime
        Name of the column containing report time

    category_column: str
        Name of the column containing category labels

    Returns
    -------
    Figure
        Displays a line plot of the monthly reports counts per category.

    Example
    --------
    plot_category_over_years(data = df,
        categories =["Graffiti,"Abfall/Sammelstelle"], 
        time_column = "reported_time",
        category_column = "service_name")
    """
    data = data.set_index(time_column)
    fig, ax = plt.subplots()
    colors=["steelblue", "seagreen",
            "sandybrown","mediumpurple",
            "lightcoral","cadetblue",
            "rosybrown","darkseagreen",
            "tan","plum"]
    i=0
    
    for cat in categories:
        filtered_data = data[data[category_column]==cat]
        monthly_reports = (
            filtered_data
                .resample("ME")
                .size()
                .reset_index(name="reports"))
        
        ax.plot( 
            monthly_reports[time_column], 
            monthly_reports["reports"],
            color=colors[i],
            label = cat,)
        
        i+=1
        
    ax.set_xlabel("Time [Year]")
    ax.set_ylabel("Number of Reports")
    ax.set_title("Monthly Reports by Category over Years")
    ax.legend() 
    
    plt.show()

    return fig


    

def plot_category_over_a_year( 
    data,
    categories,
    year,
    time_column ="Report_time",
    category_column="Category"):
    """
    Plot the monthly number of reports for categories within a specific year.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing report times and category information

    categories : list
        List of categories to include in the plot.

    time_column: datetime
        Column containing report time.

    category_column: str
        Column containing category labels.

    year : int
        Year for which the monthly reports should be plotted.


    Returns
    -------
    figure
        Displays a line plot of the monthly reports counts per category 
        for the selected year.

    Example
    -------
     plot_category_over_a_year(data = df, 
     categories =["Graffiti,"Abfall/Sammelstelle"],
     year=2025, 
     time_column ="reported_at", 
     category_column ="service_name")
    """

    data = data.set_index(time_column)
    fig, ax = plt.subplots()
    colors=["steelblue","seagreen",
            "sandybrown","mediumpurple",
            "lightcoral","cadetblue",
            "rosybrown","darkseagreen",
            "tan","plum"]
    i=0

    for cat in categories:
        filtered_data = data[data[category_column]==cat]
        report_year =( 
            filtered_data[filtered_data.index.year == year])
        monthly_reports =( 
            report_year.resample("ME")
                .size().
                reset_index(name="reports"))
        
        ax.plot(
            monthly_reports[time_column],
            monthly_reports["reports"],
            "o-",
            color=colors[i],
            label=cat,)
        i+=1
        
    ax.set_xlabel("Time [Month]")
    ax.set_ylabel("Number of Reports")
    ax.set_title("Monthly Reports by Category over a Year")
    ax.legend(loc="upper left",)
    
    plt.show()

    return fig


    

def calculate_mean_processing_time(
    data,
    category,
    category_col="Category",
    report_col="Report_time",resolved_col="Resolved_time",
    boundary_col="Neighborhoods"):
    """
    Calculate the mean processing time per neighborhood for a given category.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame containing report and resolution timestamps.

    category : str
        Category value to filter data.

    category_col: str
        Name of the column containing category labels.

    report_col: datetime
        Column containing the report timestamp.

    resolved_col: datetime
        Column containing the resolution timestamp.

    boundary_col: str
        Name of the column used for grouping

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the mean processing time in days per neighborhood

    Examples
    --------
    calculate_mean_processing_time(
        data=df, 
        category = "Abfall,Sammelstelle", 
        category_col = "service_name", 
        report_col ="reported_at", 
        resolved_col = "resolved_at", 
        boundary_col = "Neighborhoods")
    """
    filter_category = (
        data[data[category_col] == category].copy())
    
    filter_category["processing_time"] = (
        filter_category[resolved_col] 
        - filter_category[report_col])
    
    mean_days =(
    filter_category
    .groupby(boundary_col)["processing_time"]
    .mean().reset_index())
    
    mean_days["processing_time_days"] = (
        mean_days["processing_time"]
        .dt.total_seconds() / 86400)
    
    return mean_days


    

def clean_legend_labels(ax):
    """
    Clean legend labels by replacing commas with hyphen.

    Parameters
    ----------
    ax: matplotlib.axes
        Axes objects contains the legend to be cleaned

    Returns
    -------
    None
        Modifies the legend labels.
    """
    legend = ax.get_legend()
    for text in legend.get_texts():
        text.set_text(text.get_text().replace(",", "  -"))


        

def add_labels_zurich(
    ax,
    data,
    column_boundary="Neighborhoods",
    column_geometry="Geometry",
    names=None):
    """ 
    Add labels for selected Zurich neighborhoods
    
    Parameters
    ----------
    ax: matplotlib.axes
        Axes object where labels will be aded
    
    data: pandas.DataFrame
        DataFrame containing neighborhood names and geometries.

    column_boundary: str
        Column containing neighborhood names.

    column_geometry: geometry
        Column containing geometry objects of neighborhoods

    names: list
        List of neighborhood names to be labeled.

    Returns
    -------
    None
        Adds text labels using centroid coordinates of the geometries.

    Example
    -------
    add_labels_zurich(ax=ax,
    data = gdf, 
    names=["Altstetten","Oerlikon","City"])
    """
    selected_quartiere =(
        data[data["Neighborhoods"]
            .isin(names)])
    
    for i in range(len(selected_quartiere)):
        x = selected_quartiere.iloc[i][column_geometry].centroid.x
        y = selected_quartiere.iloc[i][column_geometry].centroid.y
        name = selected_quartiere.iloc[i][column_boundary]
        
        ax.text(x, y, name, fontsize=7, fontweight="light")


        

def histogram_natural_breaks(data, column,k):
    """
    Plot a histogram of a numeric column and 
    add Natural Breaks class boundaries.

    Parameters
    ----------
    data: pandas.DataFrame
        DataFrame which contains the numeric data.

    column: float
        Numeric column to visualize.

    k: int
        Number of breaks to compute using Natural Breaks

    Returns
    -------
    None
        Displays a histogram plot with vertical lines 
        which are indicating breaks.

    Examples
    --------
    histogram_natural_breaks(df,
    column ="processing_time",
    k=5)
    """
    classified_object = mapclassify.NaturalBreaks(data[column],k=k)
    breaks = classified_object.bins
    
    plt.figure(figsize=(10,5))
    plt.hist(
        data[column],
        bins=100, 
        color= "grey",
        edgecolor="black")
    
    for i in breaks:
        plt.axvline(
        i, 
        color="red", 
        linestyle="--")

    plt.title(f"Distribution of {column} with Natural Breaks")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.show()
