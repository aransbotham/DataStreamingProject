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

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1709425280377 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://awsbucketanna/step_trainer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="StepTrainerTrusted_node1709425280377",
)

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1709425317106 = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": False},
    connection_type="s3",
    format="json",
    connection_options={
        "paths": ["s3://awsbucketanna/accelerometer/trusted/"],
        "recurse": True,
    },
    transformation_ctx="AccelerometerTrusted_node1709425317106",
)

# Script generated for node SQL Query
SqlQuery0 = """
select 
ditinct
at.user,
at.x,
at.y,
at.z,
stt.serialNumber,
stt.sensorReadingTime,
stt.distanceFromObject
from stt 
JOIN at ON stt.sensorReadingTime = at.timestamp
"""
SQLQuery_node1709425337356 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={
        "at": AccelerometerTrusted_node1709425317106,
        "stt": StepTrainerTrusted_node1709425280377,
    },
    transformation_ctx="SQLQuery_node1709425337356",
)

# Script generated for node Machine Learning Curated
MachineLearningCurated_node1709425434722 = glueContext.getSink(
    path="s3://awsbucketanna/step_trainer/machine_learning/curated/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="MachineLearningCurated_node1709425434722",
)
MachineLearningCurated_node1709425434722.setCatalogInfo(
    catalogDatabase="stedi", catalogTableName="machine_learning_curated"
)
MachineLearningCurated_node1709425434722.setFormat("json")
MachineLearningCurated_node1709425434722.writeFrame(SQLQuery_node1709425337356)
job.commit()