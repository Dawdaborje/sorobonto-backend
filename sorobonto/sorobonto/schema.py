import graphene
from .settings import SOROBONTO_APPS
import importlib
import logging

# Set up logging for better debugging
logger = logging.getLogger(__name__)

# Lists to collect Query and Mutation classes from each app
queries = []
mutations = []

for app in SOROBONTO_APPS:
    try:
        # Dynamically import the app's schema module
        schema_module = importlib.import_module(f"{app}.schema")
        logger.info(f"Successfully imported schema module from {app}")

        # Check if the schema module has a 'Query' attribute and add it to the queries list
        if hasattr(schema_module, "Query"):
            queries.append(schema_module.Query)
            logger.info(f"Added Query class from {app}")

        # Check if the schema module has a 'Mutation' attribute and add it to the mutations list
        if hasattr(schema_module, "Mutation"):
            mutations.append(schema_module.Mutation)
            logger.info(f"Added Mutation class from {app}")

    except ModuleNotFoundError as e:
        # Handle the case where an app might not have a schema module
        logger.warning(
            f"No schema module found for {app}. Skipping... Exception: {str(e)}"
        )
    except Exception as e:
        # Handle other potential exceptions during import
        logger.error(f"Error importing schema from {app}: {str(e)}", exc_info=True)


# Combine all Query classes into a single Query using multiple inheritance
class Query(*queries, graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")


# Combine all Mutation classes into a single Mutation using multiple inheritance
class Mutation(*mutations, graphene.ObjectType):
    pass


# Define the final schema
schema = graphene.Schema(query=Query, mutation=Mutation)
