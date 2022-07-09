{% extends "layout.html" %}
{% block head %}
    <!-- This was the base tutorial to implement this: https://developers.arcgis.com/esri-leaflet/geocode-and-search/search-for-an-address/-->
    <link rel="stylesheet" href="https://js.arcgis.com/4.24/esri/themes/light/main.css"> 
    <script src="https://js.arcgis.com/4.24/"></script>
    <script src="{{ url_for('static', filename='new-location.js') }}"></script>
    <script>
      require(["esri/config","esri/Map", "esri/views/MapView", "esri/widgets/Search"], function (esriConfig,Map, MapView, Search) {
        esriConfig.apiKey = "{{map_key}}";
        initAutocomplete(esriConfig,Map, MapView, Search);
      });
    </script>
{% endblock %}
{% block body %}
<div id="container">
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">New Location</legend>
            {% if form.coord_latitude.errors or  form.coord_longitude.errors %}
            <div class="alert alert-danger" role="alert">
                Make sure to select a valid point in the map!
            </div>
            {% endif %}
            <div class="form-group">
                {{ form.description.label(class="form-control-label") }}
                {% if form.description.errors %}
                    {{ form.description(class="form-control form-control-lg is-invalid") }}
                    <div class="invalid-feedback">
                        {% for error in form.description.errors %}
                            <span>{{ error }}</span>
                        {% endfor %}
                    </div>
                {% else %}
                    {{ form.description(class="form-control form-control-lg") }}
                {% endif %}
            </div>
            <div class="form-group">
                {{ form.lookup_address.label(class="form-control-label") }}
                {% if form.lookup_address.errors %}
                    <small id="emailHelp" class="form-text text-muted">Use the search bar on the top-right of the map to find the address you want:</small>
                    <div class="invalid-feedback">
                        {% for error in form.lookup_address.errors %}
                            <span>{{ error }}</span>
                        {% endfor %}
                    </div>
                {% else %}
                <small id="emailHelp" class="form-text text-muted">Use the search bar on the top-right of the map to find the address you want:</small>
                {% endif %}
            </div>
        </fieldset>
        <div id="preview" style="width: 100%; height: 400px">
            <div id="viewDiv"></div>
        </div>
        <div class="form-group">
            {{ form.submit(class="btn btn-outline-info") }}
        </div>
    </form>
</div>    
{% endblock %}
