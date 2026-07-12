from loguru import logger

# TODO: funcion para verificar si la tabla listada ya esta exportada

def bronze_layer(olap_conn, oltp_db_path, bronze_path):
    logger.info("Run bronze layer")
    try:
        olap_conn.sql(f"ATTACH '{oltp_db_path}' AS oltp (TYPE sqlite);")
        olap_conn.sql(f"EXPORT DATABASE oltp TO '{bronze_path}' (FORMAT PARQUET);")
        logger.info("Bronze layer completed")
    except Exception as e:
        logger.error(f"Error in bronze layer: {e}")
