import multiprocessing
from run_model import run_model  # For TIM-Net
import numpy as np
from transcribe import *
import streamlit as st
from TRE import TRE

def your_function(_, result_list, lock, fileName):
    results = []
    # angry, fear, happy, neutral, sad = 0


    file_path = f"G:/Capstone/Capstone-Project-Modified-TIM-Net_SER/new bangla dataset/Audios/{fileName}"
    text = "Well, I can see that."
    timnet_res = run_model(file_path, _[0])
    results.append(timnet_res)
    angry, fear, happy, neutral, sad = 0, 0, 0, 0, 0
    if np.array(results).argmax() == 0:
        angry += 1
    elif np.array(results).argmax() == 1:
        fear += 1
    elif np.array(results).argmax() == 2:
        happy += 1
    elif np.array(results).argmax() == 3:
        neutral += 1
    elif np.array(results).argmax() == 4:
        sad += 1
    print(f"angry: {angry}")
    print(f"fear: {fear}")
    print(f"happy: {happy}")
    print(f"neutral: {neutral}")
    print(f"sad: {sad}")

    with lock:
        result_list.append(results[0])

    # st.title("Speech Emotion Recognition App")
    #
    # uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    #
    # if uploaded_file is not None:
    #     model_name = "EmoTexBangla"  # Replace with your actual model name
    #     file = f"G:/Capstone/Capstone-Project-Modified-TIM-Net_SER/new bangla dataset/Audios/{uploaded_file.name}"
    #     # Get user input for model prediction
    #     if st.button("Predict Emotion"):
    #         results = []
    #         trans = transcribe(file)
    #         timnet_res = run_model(file, _[0])
    #         print(timnet_res)
    #         # tre_res = TRE(trans)
    #         # temp = tre_res[0]
    #         # tre_res[0] = tre_res[3]
    #         # tre_res[3] = tre_res[1]
    #         # tre_res[1] = tre_res[2]
    #         # tre_res[2] = temp
    #
    #         # Weighted Averaging
    #         # accuracy_timnet = 0.7165
    #         # accuracy_tre = 0.7394
    #         # weight_timnet = accuracy_timnet / (accuracy_timnet + accuracy_tre)
    #         # weight_tre = accuracy_tre / (accuracy_timnet + accuracy_tre)
    #         # multi_model_res = []
    #         # for i in range(len(timnet_res)):
    #         #     multi_model_res.append((timnet_res[i] * weight_timnet) + (tre_res[i] * weight_tre))
    #         # # print(multi_model_res)
    #         # st.text(timnet_res)
    #         # st.text(transcribe)
    #
    #         # Display results
    #         # st.write(f"Predicted Emotion: {emotion}")
    #         # st.write("Class Probabilities:")
    #         # for i, prob in enumerate(probabilities):
    #         #     st.write(f"Class {i}: {prob:.4f}")
    #
    # # angry, fear, happy, neutral, sad = 0
    #         results.append(timnet_res)
    #         angry, fear, happy, neutral, sad = 0, 0, 0, 0, 0
    #         if np.array(results).argmax() == 0:
    #             angry += 1
    #         elif np.array(results).argmax() == 1:
    #             fear += 1
    #         elif np.array(results).argmax() == 2:
    #             happy += 1
    #         elif np.array(results).argmax() == 3:
    #             neutral += 1
    #         elif np.array(results).argmax() == 4:
    #             sad += 1
    #         print(f"angry: {angry}")
    #         print(f"fear: {fear}")
    #         print(f"happy: {happy}")
    #         print(f"neutral: {neutral}")
    #         print(f"sad: {sad}")
    #
    #         with lock:
    #             result_list.append(results[0])

if __name__ == "__main__":
    uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

    if st.button("Predict"):
        manager = multiprocessing.Manager()
        # Create a list to store thread instances
        processes = []
        values = list(range(1, 11))
        results = manager.list()

        lock = manager.Lock()

        # Spawn 10 threads
        for _ in range(10):
            process = multiprocessing.Process(target=your_function, args=(([values[_]]), results, lock, uploaded_file.name))
            processes.append(process)
            process.start()

        # Wait for all threads to finish
        for thread in processes:
            process.join()

        avg_result = [0, 0, 0, 0, 0]
        for i in range(len(results)):
            for j in range(len(results[i])):
                avg_result[j] += results[i][j]
        for i in range(len(avg_result)):
            avg_result[i] /= len(results)
        print(avg_result)
        st.text(avg_result)

        angry, fear, happy, neutral, sad = 0, 0, 0, 0, 0
        if np.array(avg_result).argmax() == 0:
            print("angry")
            st.text("Angry")
        elif np.array(avg_result).argmax() == 1:
            print("fear")
            st.text("Fear")
        elif np.array(avg_result).argmax() == 2:
            print("happy")
            st.text("Happy")
        elif np.array(avg_result).argmax() == 3:
            print("neutral")
            st.text("Neutral")
        elif np.array(avg_result).argmax() == 4:
            print("sad")
            st.text("Sad")
