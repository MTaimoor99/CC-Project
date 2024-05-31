import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import io #is used to write plot to a buffer
import base64 #is used to convert image to base64 format


def generate_attendance_graph(date_list,presence_indicator):
    plt.figure(figsize=(8, 8))
    plt.plot(date_list, presence_indicator)
    plt.xlabel('Dates')
    plt.ylabel('Present/Absent')
    plt.title('Attendance Graph')
    # Save the plot to a bytes object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the bytes object as a base64 string
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Close the plot to free memory
    plt.close()
    return image_base64