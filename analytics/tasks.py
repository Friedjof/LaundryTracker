import io
import base64
from datetime import timedelta

from django.utils import timezone
from django.db import models
from django.db.models import OuterRef, Subquery
from django.db.models import Count, Avg, StdDev

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from timer.models import Building
from .models import History


class Diagrams:
    @staticmethod
    def states_per_building() -> str:
        latest_status = History.objects.filter(
            machine_identifier=OuterRef('machine_identifier')
        ).order_by('-created_at')

        current_status = History.objects.filter(
            identifier=Subquery(latest_status.values('identifier')[:1])
        ).values('machine_status', 'building_identifier').annotate(total=models.Count('machine_status'))

        data = {}
        buildings = set()
        machine_statuses = set()

        for status in current_status:
            building = status['building_identifier']
            machine_status = dict(History.MACHINE_STATUS)[status['machine_status']]
            total = status['total']

            if building not in data:
                data[building] = {}
            data[building][machine_status] = total

            buildings.add(building)
            machine_statuses.add(machine_status)

        for building in buildings:
            for machine_status in machine_statuses:
                if machine_status not in data[building]:
                    data[building][machine_status] = 0

        fig, ax = plt.subplots()

        machine_statuses = list(machine_statuses)
        machine_statuses.sort()

        for building in buildings:
            building_data = [data[building][machine_status] for machine_status in machine_statuses]
            ax.bar(machine_statuses, building_data, label=f'Building {Building.objects.get(identifier=building).name}')

        ax.set_xlabel('Machine Status')
        ax.set_ylabel('Total')
        ax.set_title('Machine Status per Building')
        ax.legend()
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        buf.close()
        plt.close()

        return image_base64

    @staticmethod
    def running_machines_per_weekday_avg_linechart() -> str:
        running_machines = History.objects.filter(machine_status='R')

        weekday_counts = running_machines.annotate(
            weekday=models.functions.ExtractWeekDay('created_at')
        ).values('weekday', 'building').annotate(total=Count('identifier'))

        weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        buildings = list(set(entry['building'] for entry in weekday_counts))
        data = {building: [0] * 7 for building in buildings}
        total_days = {building: [0] * 7 for building in buildings}

        for entry in weekday_counts:
            building = entry['building']
            weekday = entry['weekday'] - 1
            data[building][weekday] += entry['total']
            total_days[building][weekday] += 1

        avg_counts = {building: [data[building][i] / total_days[building][i] if total_days[building][i] != 0 else 0 for i in range(7)] for building in buildings}

        fig, ax = plt.subplots()
        for building in buildings:
            ax.plot(weekdays, avg_counts[building], marker='o', label=building)

        ax.set_xlabel('Weekday')
        ax.set_ylabel('Average Number of Running Machines')
        ax.set_title('Average Running Machines per Weekday by Building')
        ax.legend()
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        buf.close()
        plt.close()

        return image_base64

    @staticmethod
    def map_weekday_hour_diagram() -> str:
        """
        This method will create a diagram that shows the average number of running machines per weekday and hour.
        This is plotted as a heatmap.
        :return: The base64 encoded image of the diagram
        """
        running_machines = History.objects.filter(machine_status='R')

        # Annotate with the weekday and hour
        weekday_hour_counts = running_machines.annotate(
            weekday=models.functions.ExtractWeekDay('created_at'),
            hour=models.functions.ExtractHour('created_at')
        ).values('weekday', 'hour').annotate(total=Count('identifier'))

        # Prepare data for plotting
        heatmap_data = [[0 for _ in range(24)] for _ in range(7)]  # 7 days, 24 hours

        for entry in weekday_hour_counts:
            heatmap_data[entry['weekday'] - 1][entry['hour']] = entry[
                'total']  # Weekday is 1-based (1=Sunday, 7=Saturday)

        # Create the heatmap
        fig, ax = plt.subplots(figsize=(12, 7))
        cax = ax.matshow(heatmap_data, cmap='YlGnBu')

        # Set axis labels
        ax.set_xticks(range(24))
        ax.set_yticks(range(7))
        ax.set_xticklabels(range(24))
        ax.set_yticklabels(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])

        # Add color bar
        fig.colorbar(cax)

        ax.set_xlabel('Hour of the Day')
        ax.set_ylabel('Weekday')
        ax.set_title('Average Number of Running Machines per Weekday and Hour')
        plt.tight_layout()

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image to base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        buf.close()
        plt.close()

        return image_base64

    @staticmethod
    def last_3_weeks_of_running_machines() -> str:
        three_weeks_ago = timezone.now() - timedelta(weeks=3)
        running_machines = History.objects.filter(machine_status='R', created_at__gte=three_weeks_ago)

        daily_counts = running_machines.annotate(
            date=models.functions.TruncDate('created_at')
        ).values('date', 'building').annotate(total=Count('identifier')).order_by('date')

        dates = list(set(entry['date'] for entry in daily_counts))
        dates.sort()
        buildings = list(set(entry['building'] for entry in daily_counts))
        data = {building: [0] * len(dates) for building in buildings}

        for entry in daily_counts:
            date_index = dates.index(entry['date'])
            building = entry['building']
            data[building][date_index] = entry['total']

        fig, ax = plt.subplots()
        for building in buildings:
            ax.plot(dates, data[building], marker='o', label=building)

        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Running Machines')
        ax.set_title('Running Machines in the Last 3 Weeks by Building')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        buf.close()
        plt.close()

        return image_base64

    @staticmethod
    def last_3_weeks_of_machine_status() -> str:
        from django.utils import timezone
        from datetime import timedelta

        # Calculate the date three weeks ago
        three_weeks_ago = timezone.now() - timedelta(weeks=3)

        # Filter for machine statuses in the last three weeks
        machine_statuses = History.objects.filter(created_at__gte=three_weeks_ago)

        # Annotate with the date and count the occurrences for each status
        daily_counts = machine_statuses.annotate(
            date=models.functions.TruncDate('created_at')).values('date','machine_status').annotate(
            total=Count('identifier')
        ).order_by('date')

        # Prepare data for plotting
        dates = []
        status_counts = {status[0]: [] for status in History.MACHINE_STATUS}

        for entry in daily_counts:
            date = entry['date']
            status = entry['machine_status']
            total = entry['total']

            if date not in dates:
                dates.append(date)
                for status_list in status_counts.values():
                    status_list.append(0)

            status_counts[status][-1] = total

        # Create the line chart
        fig, ax = plt.subplots()
        for status, counts in status_counts.items():
            ax.plot(dates, counts, marker='o', label=dict(History.MACHINE_STATUS)[status])

        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Machines')
        ax.set_title('Machine Statuses in the Last 3 Weeks')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Set date format on x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image to base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        buf.close()
        plt.close()

        return image_base64

    @staticmethod
    def used_machines_per_type_and_building() -> str:
        # Query to get the count of machines per type and building
        machine_counts = History.objects.filter(machine_status='R').values('building', 'machine_number').annotate(
            total=Count('machine_identifier'))

        # Prepare data for plotting
        buildings = list(set(entry['building'] for entry in machine_counts))
        machine_numbers = list(set(entry['machine_number'] for entry in machine_counts))
        data = {building: {machine_number: 0 for machine_number in machine_numbers} for building in buildings}

        for entry in machine_counts:
            data[entry['building']][entry['machine_number']] = entry['total']

        # Create the heatmap
        fig, ax = plt.subplots()
        heatmap_data = [[data[building][machine_number] for machine_number in machine_numbers] for building in buildings]

        # if Invalid shape (0,) for image data
        if len(heatmap_data) == 0:
            heatmap_data = [[0]]

        cax = ax.matshow(heatmap_data, cmap='YlGnBu')

        # Set axis labels
        ax.set_xticks(range(len(machine_numbers)))
        ax.set_yticks(range(len(buildings)))
        ax.set_xticklabels(machine_numbers)
        ax.set_yticklabels(buildings)

        # Add color bar
        fig.colorbar(cax)

        ax.set_xlabel('Machine Number')
        ax.set_ylabel('Building')
        ax.set_title('Used Machines per Number and Building')
        plt.tight_layout()

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image to base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        buf.close()
        plt.close()

        return image_base64

    @staticmethod
    def avg_running_time_per_machine_type() -> str:
        # Query to get the average running time and standard deviation per machine type
        avg_times = History.objects.filter(machine_status='R').values('machine_type').annotate(
            avg_time=Avg('timer'),
            stddev_time=StdDev('timer')
        )

        min_timers = History.objects.filter(machine_status='R').values('machine_type').annotate(
            min_time=models.Min('timer')
        )

        max_timers = History.objects.filter(machine_status='R').values('machine_type').annotate(
            max_time=models.Max('timer')
        )

        # Prepare data for plotting
        machine_types = [dict(History.MACHINE_TYPE)[entry['machine_type']] for entry in avg_times]
        avg_times_values = [entry['avg_time'] for entry in avg_times]
        min_times_values = [entry['min_time'] for entry in min_timers]
        max_times_values = [entry['max_time'] for entry in max_timers]

        # Create the bar chart with error bars
        fig, ax = plt.subplots()
        tmp_y_err = [
            (avg_times_values[i] - min_times_values[i], max_times_values[i] - avg_times_values[i])
            for i in range(len(avg_times_values))
        ]
        tmp_y_err = list(zip(*tmp_y_err))  # Transpose the list of tuples to match the required shape

        ax.bar(machine_types, avg_times_values, yerr=tmp_y_err, capsize=5)

        ax.set_xlabel('Machine Type')
        ax.set_ylabel('Average Running Time (minutes)')
        ax.set_title('Average Running Time per Machine Type with Standard Deviation')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image to base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        buf.close()
        plt.close()

        return image_base64

    @staticmethod
    def machine_status_distribution() -> str:
        machine_status_colors = {
            'A': 'green',
            'R': 'blue',
            'F': 'gray',
            'D': 'red',
            'B': 'yellow',
            'U': 'black',
        }

        # Query to get the count of each machine status
        status_counts = History.objects.values('machine_status').annotate(total=Count('identifier'))

        # Prepare data for plotting
        statuses = [dict(History.MACHINE_STATUS)[entry['machine_status']] for entry in status_counts]
        totals = [entry['total'] for entry in status_counts]
        colors = [machine_status_colors[entry['machine_status']] for entry in status_counts]

        # Create the pie chart
        fig, ax = plt.subplots()
        ax.pie(totals, labels=statuses, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title('Machine Status Distribution')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image to base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        buf.close()
        plt.close()

        return image_base64

    @staticmethod
    def machine_types_per_building() -> str:
        # Subquery to get the latest status for each machine
        latest_status = History.objects.filter(
            machine_identifier=OuterRef('machine_identifier')
        ).order_by('-created_at')

        # Query to get the count of each machine type per building with the latest status
        type_counts = History.objects.filter(
            identifier=Subquery(latest_status.values('identifier')[:1])
        ).values('building', 'machine_type').annotate(total=Count('identifier'))

        # Prepare data for plotting
        buildings = list(set(entry['building'] for entry in type_counts))
        machine_types = list(set(entry['machine_type'] for entry in type_counts))
        data = {building: {machine_type: 0 for machine_type in machine_types} for building in buildings}

        for entry in type_counts:
            data[entry['building']][entry['machine_type']] = entry['total']

        # Create the stacked bar chart
        fig, ax = plt.subplots()
        bottom = [0] * len(buildings)
        for machine_type in machine_types:
            counts = [data[building][machine_type] for building in buildings]
            ax.bar(buildings, counts, bottom=bottom, label=dict(History.MACHINE_TYPE)[machine_type])
            bottom = [i + j for i, j in zip(bottom, counts)]

        ax.set_xlabel('Building')
        ax.set_ylabel('Total Machines')
        ax.set_title('Machine Types per Building')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image to base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')

        buf.close()
        plt.close()

        return image_base64