import numpy as np
import lumicks.pylake as lk


def init():
    print("\033[1;32m \n")
    print("*********************************************************")
    print("Made by V.B. Verduijn; v.b.verduijn@rug.nl")
    print("Version 1.3")
    print("Do not reproduce without permission")
    print("Github: https://github.com/VBVerduijn/force-tiff-merger")
    print("*********************************************************")
    print("\033[1;37m \n")
    print("All plugins have been initialised")
    return False


def pre_proc(data_):
    # Importing the datastream
    fn_ = f"{data_}"
    int_data_ = lk.File(fn_)  # read in data
    print(int_data_)
    chosen_ = input("What variable should be exported as the y data? (time = x-data): ")
    chosen_marker_ = input("What is the marker name? ['n' for no marker data necessary]: ")
    if chosen_marker_ != "n":
        downsampling_ = input("By what number should the data be downsampled? [>=1]: ")
        print("Data is being downsampled! This may take some time.")
        time_ = getattr(int_data_, chosen_).downsampled_by(int(downsampling_)).timestamps / 1e9
        time_ = time_ - time_[0]
        data_ext_ = np.array([time_,getattr(int_data_, chosen_).downsampled_by(int(downsampling_)).data], dtype=np.float64).transpose()

        marker_ = int_data_.markers[chosen_marker_]
        start_vid = marker_.start / 1e9 - (getattr(int_data_, chosen_).downsampled_by(int(downsampling_)).timestamps / 1e9)[0]
        end_vid = marker_.stop / 1e9 - (getattr(int_data_, chosen_).downsampled_by(int(downsampling_)).timestamps / 1e9)[0]
    else:
        downsampling_ = input("By what number should the data be downsampled? [>=1]: ")
        print("Data is being downsampled! This may take some time.")
        time_ = getattr(int_data_, chosen_).downsampled_by(int(downsampling_)).timestamps / 1e9
        time_ = time_ - time_[0]
        data_ext_ = np.array([time_, getattr(int_data_, chosen_).downsampled_by(int(downsampling_)).data],
                             dtype=np.float64).transpose()
        start_vid = "N/A"
        end_vid = "N/A"
    return data_ext_, start_vid, end_vid


if __name__ == '__main__':
    init()

    data_file = input("What is the data-file name? [FULL PATH] ")
    data_ext,start,stop = pre_proc(data_file)
    file_loc = input("What should be the file output directory? [Full Path]: ")
    file_name = input("What should be the file-name [without extension!]: ")
    print("File is being outputted! Do not close the window.")
    try:
        print(f"The number of datapoints is: {data_ext.shape}")
        print(f"The video started at t = {start} s [from 0s (1st datapoint)]")
        print(f"The video stopped at t = {stop} s [from 0s (1st datapoint)]")
        np.savetxt(f"{file_loc}/{file_name}.csv", data_ext, delimiter=",")
    except IOError:
        print(f"The Specified folder [{file_loc}] does not exist!")
    finally:
        print("File has been saved, you can now close the window.")


