from ffmpeg import FFmpeg, Progress
import os

def main():
    path = os.path.abspath("long.mp4")
    print(path)

    fileObject = open(path)

    print("file:", (fileObject))
    
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("pipe:0")
        .output(
            "out.wav",
            {"codec:a": "pcm_s16le"},
            vn=None,
            f="wav",
        )
    )

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        print(progress)

    ffmpeg.execute(fileObject)

main()
