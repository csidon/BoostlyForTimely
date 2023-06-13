# The staff package will be extremely light for the MVP. It will assume: 
# -- That each User will only have one Staff
# -- The staff details are replicated from the User's details during account creation  # Functionality in utils folder
# -- There will be no display pic for Staff for the MVP
# -- There will stil be a separate table for User and Staff
# -- There is no account setup process for Staff - This will have to be done manually by a Boostly team member


# The basic relationship for the models are:
# 1 User -> 1 Staff (for the MVP ONLY)
# 1 Staff -> * Clients
# 1 Client -> * Alerts