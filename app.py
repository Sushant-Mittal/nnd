import psutil
import time
from flask import Flask, render_template
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    recv_lst = []
    sent_lst = []
    total_lst = []
    time_lst = []

    last_received = psutil.net_io_counters().bytes_recv
    last_sent = psutil.net_io_counters().bytes_sent
    last_total = last_received + last_sent

    recv_lst.append(0)
    sent_lst.append(0)
    total_lst.append(0)
    time_lst.append(0)

    fig, ((ax1), (ax2), (ax3)) = plt.subplots(nrows=3, ncols=1, figsize=(10, 10), sharex=True)
    graph1 = ax1.plot(recv_lst, time_lst)[0]
    graph2 = ax2.plot(sent_lst, time_lst)[0]
    graph3 = ax3.plot(total_lst, time_lst)[0]

    ax1.set_xlim([0, 120])
    ax2.set_xlim([0, 120])
    ax3.set_xlim([0, 120])

    ax1.set_ylim([0, 1])
    ax2.set_ylim([0, 1])
    ax3.set_ylim([0, 1])

    ax1.set(title="Received data (MB) per second", ylabel="MB")
    ax2.set(title="Sent data (MB) per second", ylabel="MB")
    ax3.set(title="Total transaction (MB) per second", ylabel="MB")

    time_counter = 0

    dspeed_text = "Download Speed: " + str(0) + " MB/s"
    uspeed_text = "Upload Speed: " + str(0) + "MB/s"

    text1 = ax1.text(0, 1, dspeed_text, transform=ax1.transAxes, fontsize=14, verticalalignment="top")
    text2 = ax2.text(0, 1, uspeed_text, transform=ax2.transAxes, fontsize=14, verticalalignment="top")

    def update(frame):
        nonlocal time_counter, last_received, last_sent, last_total, recv_lst, sent_lst, total_lst, graph1, graph2, graph3

        bytes_received = psutil.net_io_counters().bytes_recv
        bytes_sent = psutil.net_io_counters().bytes_sent
        bytes_total = bytes_received + bytes_sent

        new_received = bytes_received - last_received
        new_sent = bytes_sent - last_sent
        new_total = bytes_total - last_total

        mb_new_received = new_received / 1024 / 1024
        mb_new_sent = new_sent / 1024 / 1024
        mb_new_total = new_total / 1024 / 1024

        print(f"At time instant {time_counter} seconds, {mb_new_received:.2f} MB received, {mb_new_sent:.2f} MB sent, {mb_new_total:.2f} MB total")
        time_counter += 1

        recv_lst.append(mb_new_received)
        sent_lst.append(mb_new_sent)
        total_lst.append(mb_new_total)
        time_lst.append(time_counter)

        ax1.set_ylim([min(recv_lst), max(recv_lst)])
        ax2.set_ylim([min(sent_lst), max(sent_lst)])
        ax3.set_ylim([min(total_lst), max(total_lst)])

        ax1.set_xlim([min(time_lst), max(time_lst)])
        ax2.set_xlim([min(time_lst), max(time_lst)])
        ax3.set_xlim([min(time_lst), max(time_lst)])

        download_speed = recv_lst[-1]
        upload_speed = sent_lst[-1]

        dspeed_text = "Download Speed: " + str(round(download_speed, 2)) + " MB/s"
        uspeed_text = "Upload Speed: " + str(round(upload_speed, 2)) + "MB/s"

        graph1.set_xdata(time_lst)
        graph1.set_ydata(recv_lst)

        graph2.set_xdata(time_lst)
        graph2.set_ydata(sent_lst)

        graph3.set_xdata(time_lst)
        graph3.set_ydata(total_lst)

        text1.set_text(dspeed_text)
        text2.set_text(uspeed_text)

        plt.draw()

        last_received = bytes_received
        last_sent = bytes_sent
        last_total = bytes_total

        time.sleep(1)

    anim = FuncAnimation(fig, update)
    plt.close(fig)  # Prevents plt.show() from blocking
    return plt.figure().to_html()

if __name__ == '_main_':
    app.run(debug=True)