import csv
import threading
from pytube import YouTube


def download_video(url, name, row):
    print("Starting the download of", name)
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()  # Get the highest resolution stream
        video.download()  # Download the video
        print("Video downloaded successfully!")
        row.append("completed")  # Append "completed" status to the row
    except Exception as e:
        print("Error:", str(e))
        row.append("failed")  # Append "failed" status to the row

    print("Done with", name)


# Prompt the user to enter the CSV file path
# csv_file = input("Enter the path of the CSV file: ")
csv_file = "./techdose.csv"

# Read the CSV file and download videos
with open(csv_file, 'r', newline='') as file:
    reader = csv.reader(file)
    rows = list(reader)  # Read all rows into a list
    header = rows[0]  # Get the header row
    header.append("Status")  # Add a new column header for status

    threads = []
    max_threads = 3  # Number of maximum threads to download videos concurrently

    for row in rows[1:]:
        # Assuming the third column contains the YouTube video URLs
        video_url = row[2]
        name = row[1]
        # Create a new thread for each video
        thread = threading.Thread(
            target=download_video, args=(video_url, name, row))
        threads.append(thread)
        thread.start()

        # Wait until the maximum number of threads is reached before starting new threads
        if len(threads) >= max_threads:
            for thread in threads:
                thread.join()
            threads = []

    # Wait for any remaining threads to complete
    for thread in threads:
        thread.join()

# Write the updated rows to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("Download process completed and status updated in the CSV file.")
