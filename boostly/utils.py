"""
This method cleans up the session object and closes the connection pool using the dispose 
method. This is defined here since it's used almost throughout the app
"""
def cleanup(session):
    session.close()
    # engine_container.dispose()
    print(">>> DB session closed")