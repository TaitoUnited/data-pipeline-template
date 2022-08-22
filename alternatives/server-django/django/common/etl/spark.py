import os


# Prepares Spark for storage bucket connection
def init_spark(
    sc,
    bucket_type=os.environ.get("STORAGE_TYPE", "s3"),
    key1=os.environ.get("STORAGE_ACCESS_KEY"),
    key2=os.environ.get("STORAGE_SECRET_KEY"),
    endpoint=os.environ.get("STORAGE_ENDPOINT"),
):
    conf = sc._jsc.hadoopConfiguration()

    # AWS S3 or Minio with s3a
    if bucket_type == "s3":
        # Set credentials for S3 bucket access
        conf.set("fs.s3a.access.key", key1)
        conf.set("fs.s3a.secret.key", key2)

        # Set storage endpoint if we are connecting to Minio container
        # instead of AWS S3
        if endpoint:
            conf.set("fs.s3a.endpoint", endpoint)
            conf.set("fs.s3a.connection.ssl.enabled", "false")
            conf.set("fs.s3a.path.style.access", "true")

        return "s3a://"

    # Azure blob storage
    elif bucket_type == "azure":
        conf.set(
            "fs.azure.account.key." + key1 + ".blob.core.windows.net", key2
        )
        return "wasbs://"

    else:
        raise Exception("Bucket type not supported: " + bucket_type)
