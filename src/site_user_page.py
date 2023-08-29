import os
import streamlit as st
from datetime import datetime, timedelta, time, timezone
from pvsite_datamodel.connection import DatabaseConnection
from pvsite_datamodel.read import (
    get_all_sites,
    get_pv_generation_by_sites,
    get_latest_forecast_values_by_site,
    get_user_by_email,
    get_site_by_uuid,
    get_site_group_by_name,
)
from get_data import get_all_users, get_all_site_groups, attach_site_group_to_user


import plotly.graph_objects as go


# get_user_details(): select user and show details for that user => user_uuid, email, sitegroups attached
 

# add_site_group_to_user(): attach a sitegorup to a user/ use my name as a testuser and add sitegroup 
# add_site_to_sitegroup(): attach a site to a sitegroup
# add_all_sites_ocf_sitegroup(): attach all sites to ocf sitegroup 

def site_user_page():
    """Page for site and user overview and admin"""
    st.markdown(
        f'<h1 style="color:#FFD053;font-size:48px;">{"OCF Analysis Dashboard"}</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<h1 style="color:#63BCAF;font-size:48px;">{"Site and User Page"}</h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<h1 style="color:#63BCAF;font-size:32px;">{"Get User Details"}</h1>',
        unsafe_allow_html=True,
    )
    # dropdown to explain what the page is for 

    # get the user details
    url = os.environ["SITES_DB_URL"]
    connection = DatabaseConnection(url=url, echo=True)
    with connection.get_session() as session:
      # get the user details
      users = get_all_users(session=session)
      user_list = [user.email for user in users]
      email = st.selectbox("Enter email of user you want to know about.", user_list)
      site_groups = get_all_site_groups(session=session)
      site_groups = [site_groups.site_group_name for site_groups in site_groups]
      def get_user_details(): 
        """Get the user details from the database"""
        user_details = get_user_by_email(session=session,
                                         email=email)
        user_site_group = user_details.site_group.site_group_name
        user_sites = [str(site.site_uuid) for site in user_details.site_group.sites]
        
        st.markdown(
          f'<h1 style="color:#63BCAF;font-size:48px;">{"site group: "}{user_site_group}</h1>',
          unsafe_allow_html=True,
        )
        st.write("Here are the sites in the", user_site_group, "group:", user_sites, "This site group contains", len(user_sites), "sites.")

        # get details for a single site
      def get_site_details():
        """Get the site details from the database"""
        site_uuid = get_site_by_uuid(session=session, site_uuid=site_selection)
        site_capacity = site_uuid.capacity_kw
        site_group = site_uuid.site_groups[0].site_group_name
        st.write("Here are the details for site", site_selection, ":", site_capacity, "kW")
        st.write("This site is in sitegroup", site_group)

      
      def get_site_group_details():
        """Get the site group details from the database"""
        site_group_uuid = get_site_group_by_name(session=session, site_group_name=site_group_selection)
        site_group_sites = [str(site.site_uuid) for site in site_group_uuid.sites]
        site_group_users = [user.email for user in site_group_uuid.users]
        st.write("Here are the details for site group", site_group_selection, ":", site_group_sites, site_group_users)
        st.write("This site group contains", len(site_group_sites), "sites and", len(site_group_users), "users.")
      
      def add_site_group_to_user():
        """Add a site group to a user"""
        new_group_for_user = attach_site_group_to_user(session=session, email=email, site_group_name=site_group_selection)
        new_group_for_user = new_group_for_user.site_group_uuid
        print(new_group_for_user)
        st.write("The site group has been added to the user.")


    if st.button("Get user details"):
        get_user_details()
        if st.button("Clear user details"):
            st.empty()
    
    # get_site_details(): select a site and see the details for that site => dropdown menu from previous page 
    # get_site_group_details():select a sitegroup and show what users are attached and what sites are attached => dropdown menu with sitegroup names
    st.markdown(
        f'<h1 style="color:#63BCAF;font-size:32px;">{"Get Site Details"}</h1>',
        unsafe_allow_html=True,
    )
    site_selection = st.text_input("Enter site uuid of site you want to know about.",)
    if st.button("Get site details"):
        get_site_details()
        if st.button("Clear site details"):
            st.empty()

    st.markdown(
        f'<h1 style="color:#63BCAF;font-size:32px;">{"Get Site Group Details"}</h1>',
        unsafe_allow_html=True,
    )
    site_group_selection = st.selectbox("Enter the site group name.", site_groups)
    if st.button("Get site group details"):
        get_site_group_details()
        if st.button("Clear site group details"):
            st.empty()

    st.markdown(
        f'<h1 style="color:#63BCAF;font-size:32px;">{"Add Site Group to User"}</h1>',
        unsafe_allow_html=True,
    )
    
    site_group_selection = st.selectbox("Select site group you'll add to user", site_groups)
    email = st.selectbox("Select user you'll add site group to", user_list)

    if st.button("Add site group to user"):
        add_site_group_to_user()
        if st.button("Clear user details"):
            st.empty()

    st.markdown(
        f'<h1 style="color:#63BCAF;font-size:32px;">{"Add Site to Site Group"}</h1>',
        unsafe_allow_html=True,
    )

    if st.button("Add site to site group"):
        print("the site has been added")
        if st.button("Clear user details"):
            st.empty()
    
    st.markdown(
        f'<h1 style="color:#63BCAF;font-size:32px;">{"Delete a Site"}</h1>',
        unsafe_allow_html=True,
    )

    if st.button("Delete site"):
        print("the site has been deleted")
        if st.button("Clear user details"):
            st.empty()
        
      
            
       
  
