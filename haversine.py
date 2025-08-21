import streamlit as st
import folium
import math
import streamlit.components.v1 as components

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

# Set page config
st.set_page_config(
    page_title="Coordinate Distance Calculator",
    page_icon="🌍",
    layout="wide"
)

# App title
st.title("🌍 Coordinate Distance Calculator")
st.write("Enter two coordinates to see them on a map and calculate the distance between them.")

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 First Coordinate")
    lat1 = st.number_input(
        "Latitude 1", 
        value=40.7128, 
        min_value=-90.0, 
        max_value=90.0, 
        step=0.0001,
        format="%.4f",
        help="Enter latitude between -90 and 90"
    )
    lon1 = st.number_input(
        "Longitude 1", 
        value=-74.0060, 
        min_value=-180.0, 
        max_value=180.0, 
        step=0.0001,
        format="%.4f",
        help="Enter longitude between -180 and 180"
    )

with col2:
    st.subheader("📍 Second Coordinate")
    lat2 = st.number_input(
        "Latitude 2", 
        value=34.0522, 
        min_value=-90.0, 
        max_value=90.0, 
        step=0.0001,
        format="%.4f",
        help="Enter latitude between -90 and 90"
    )
    lon2 = st.number_input(
        "Longitude 2", 
        value=-118.2437, 
        min_value=-180.0, 
        max_value=180.0, 
        step=0.0001,
        format="%.4f",
        help="Enter longitude between -180 and 180"
    )

# Calculate distance
distance_km = haversine_distance(lat1, lon1, lat2, lon2)
distance_miles = distance_km * 0.621371

# Display results
st.subheader("📏 Distance Calculation")
col_dist1, col_dist2 = st.columns(2)

with col_dist1:
    st.metric("Distance (Kilometers)", f"{distance_km:.2f} km")

with col_dist2:
    st.metric("Distance (Miles)", f"{distance_miles:.2f} miles")

# Create map
st.subheader("🗺️ Map View")

# Calculate center point for map
center_lat = (lat1 + lat2) / 2
center_lon = (lon1 + lon2) / 2

# Create folium map
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=4,
    tiles='OpenStreetMap'
)

# Add markers for both coordinates
folium.Marker(
    [lat1, lon1],
    popup=f"Point 1<br>Lat: {lat1}<br>Lon: {lon1}",
    tooltip="First Coordinate",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

folium.Marker(
    [lat2, lon2],
    popup=f"Point 2<br>Lat: {lat2}<br>Lon: {lon2}",
    tooltip="Second Coordinate",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Add a line connecting the two points
folium.PolyLine(
    locations=[[lat1, lon1], [lat2, lon2]],
    color='green',
    weight=3,
    opacity=0.8,
    popup=f"Distance: {distance_km:.2f} km"
).add_to(m)

# Display map in Streamlit using HTML component
components.html(m._repr_html_(), height=500)

# Display coordinate information
st.subheader("📋 Coordinate Information")
coord_col1, coord_col2 = st.columns(2)

with coord_col1:
    st.info(f"""
    **First Coordinate:**
    - Latitude: {lat1}°
    - Longitude: {lon1}°
    """)

with coord_col2:
    st.info(f"""
    **Second Coordinate:**
    - Latitude: {lat2}°
    - Longitude: {lon2}°
    """)

# Additional information
with st.expander("ℹ️ About the Haversine Formula"):
    st.write("""
    The **Haversine formula** calculates the shortest distance between two points on a sphere 
    (like Earth) given their latitude and longitude coordinates. 
    
    The formula accounts for the Earth's curvature and provides the "great circle" distance, 
    which is the shortest distance between two points on the surface of a sphere.
    
    **Formula:**
    ```
    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    c = 2 ⋅ atan2( √a, √(1−a) )
    d = R ⋅ c
    ```
    
    Where:
    - φ is latitude
    - λ is longitude  
    - R is Earth's radius (≈6,371 km)
    - Δ represents the difference between coordinates
    """)

# Footer
st.markdown("---")
