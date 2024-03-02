import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Customer Trusted
CustomerTrusted_node1709419631710 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://awsbucketanna/customer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="CustomerTrusted_node1709419631710",
)

# Script generated for node Step Trainer
StepTrainer_node1709420458293 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://awsbucketanna/step_trainer/landing/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainer_node1709420458293",
)

# Script generated for node Join to Opted In Users
JointoOptedInUsers_node1709420554980 = Join.apply(
    frame1=CustomerTrusted_node1709419631710,
    frame2=StepTrainer_node1709420458293,
    keys1=["serialnumber"],
    keys2=["serialnumber"],
    transformation_ctx="JointoOptedInUsers_node1709420554980",
)

# Script generated for node Keep Columns Needed
SqlQuery0 = """
select sensorReadingTime,
serialNumber,
distanceFromObject
from opted_in_join
"""
KeepColumnsNeeded_node1709422998378 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={"opted_in_join": JointoOptedInUsers_node1709420554980},
    transformation_ctx="KeepColumnsNeeded_node1709422998378",
)

# Script generated for node Trusted Accelerometer
TrustedAccelerometer_node1709420602466 = glueContext.getSink(
    path="s3://awsbucketanna/accelerometer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="TrustedAccelerometer_node1709420602466",
)
TrustedAccelerometer_node1709420602466.setCatalogInfo(
    catalogDatabase="stedi", catalogTableName="accelerometer_trusted"
)
TrustedAccelerometer_node1709420602466.setFormat("json")
TrustedAccelerometer_node1709420602466.writeFrame(KeepColumnsNeeded_node1709422998378)
job.commit()