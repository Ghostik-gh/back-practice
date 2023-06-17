from rabbit import channel


if __name__=="__main__":
    channel.start_consuming()
    channel.close()
