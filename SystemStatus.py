import socket
import psutil
import GPUtil
from tkinter import *
import requests

def get_system_status():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    gpu_usage = get_gpu_usage() if GPUtil.getGPUs() else ['N/A']
    disk_usage = psutil.disk_usage('/').percent
        
    ip_address = get_ip_address()
    location = get_location()
    
    return cpu_usage, memory_usage, gpu_usage, disk_usage, ip_address, location

def get_ip_address(): 
    # Get the network IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def get_gpu_usage():
    gpus = GPUtil.getGPUs()
    gpu_usage = []
    for gpu in gpus:
        gpu_usage.append(gpu.load * 100)
    return gpu_usage

def get_location(): 
    # Use an API to get the location based on IP address
    response = requests.get("https://ipapi.co/json/")
    data = response.json()
    return data['city'] + ', ' + data['region'] + ', ' + data['country']

def update_status_labels():
    cpu_usage, memory_usage, gpu_usage, disk_usage, ip_address, location = get_system_status()
    
    cpu_label.config(text=f'CPU Usage: {cpu_usage}%')
    memory_label.config(text=f'Memory Usage: {memory_usage}%')
    gpu_label.config(text=f'GPU Usage: {gpu_usage[0]}%')
    disk_label.config(text=f'Disk Usage: {disk_usage}%')    
    ip_label.config(text=f'IP Address: {ip_address}')
    location_label.config(text=f'Location: {location}')

    root.after(1000, update_status_labels)

root = Tk()
root.title('System Status')



cpu_label = Label(root, text='', bg='black', fg='white')
cpu_label.pack()

memory_label = Label(root, text='', bg='black', fg='white')
memory_label.pack()

gpu_label = Label(root, text='', bg='black', fg='white')
gpu_label.pack()

disk_label = Label(root, text='', bg='black', fg='white')
disk_label.pack()



ip_label = Label(root, text='', bg='black', fg='white')
ip_label.pack()

location_label = Label(root, text='', bg='black', fg='white')
location_label.pack()

# Change the background color of the main window
root.configure(background='black')

update_status_labels()

root.mainloop()
