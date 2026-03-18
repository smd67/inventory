import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
});

// This method handles the REST call to insert the note into the database.
export const activity_log = async (item_type, item_name, description, technician_name=null) => {
  console.log('IN activity_log');
  const config = {
      headers: {
          'Content-Type': 'application/json'
      }
  };
  const requestBody = {
      item_type: item_type,
      item_name: item_name,
      description: description,
      technician_name
  };
  console.log("requestBody=" + JSON.stringify(requestBody));
  try {
      const response = await api.post('/activity-log', requestBody, config);
      console.log("status=" + response.status);
  } catch (e) {
      console.error('Error inserting data:', e);
  }
  console.log('OUT activity_log');
};

// Retrieve base units from the database.
export const fetchBaseUnitNames = async () => {
  let baseUnitNames = [];
  const config = {
      headers: {
          'Content-Type': 'application/json'
      }
  };

  try {
      const response = await api.get('/get-base-units-names', config);
      baseUnitNames = response.data;
  } catch (e) {
      console.error('Error fetching data:', e);
  }
  return baseUnitNames;
};

// Retrieve base unit from the database.
export const fetchBaseUnitById = async (id) => {
  let baseUnit = null;
  const config = {
      headers: {
          'Content-Type': 'application/json'
      }
  };
  const requestBody = {
      id: id
  };

  try {
      const response = await api.post('/get-base-unit-by-id', requestBody, config);
      baseUnit = response.data;
  } catch (e) {
      console.error('Error fetching data:', e);
  }
  return baseUnit;
};

// Retrieve camera from the database.
export const fetchCameraById = async (id) => {
  let camera = null;
  const config = {
    headers: {
        'Content-Type': 'application/json'
    }
  };
  const requestBody = {
      id: id
  };

  try {
      const response = await api.post('/get-camera-by-id', requestBody, config);
      camera = response.data;
  } catch (e) {
      console.error('Error fetching data:', e);
  }
  return camera;
};

// Retrieve camera from the database.
export const fetchOtherItemById = async (id) => {
  let otherItem = null;
  const config = {
    headers: {
        'Content-Type': 'application/json'
    }
  };
  const requestBody = {
      id: id
  };

  try {
      const response = await api.post('/get-other-item-by-id', requestBody, config);
      otherItem = response.data;
  } catch (e) {
      console.error('Error fetching data:', e);
  }
  return otherItem;
};
export default api;