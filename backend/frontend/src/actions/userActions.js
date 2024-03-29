import axios from 'axios'
import {
    USER_LOGIN_REQUEST,
    USER_LOGIN_SUCCESS,
    USER_LOGIN_FAIL,

    USER_LOGOUT,

    USER_REGISTER_REQUEST,
    USER_REGISTER_SUCCESS,
    USER_REGISTER_FAIL,

    USER_DETAILS_REQUEST,
    USER_DETAILS_SUCCESS,
    USER_DETAILS_FAIL,
    USER_DETAILS_RESET,

    USER_ADDRESS_DETAILS_REQUEST,
    USER_ADDRESS_DETAILS_SUCCESS,
    USER_ADDRESS_DETAILS_FAIL,
    USER_ADDRESS_DETAILS_RESET,

    USER_UPDATE_PROFILE_REQUEST,
    USER_UPDATE_PROFILE_SUCCESS,
    USER_UPDATE_PROFILE_FAIL,

    USER_LIST_REQUEST,
    USER_LIST_SUCCESS,
    USER_LIST_FAIL,
    USER_LIST_RESET,

    USER_DELETE_REQUEST,
    USER_DELETE_SUCCESS,
    USER_DELETE_FAIL,

    USER_UPDATE_REQUEST,
    USER_UPDATE_SUCCESS,
    USER_UPDATE_FAIL,
} from '../constants/userConstants'
import {
    CART_CLEAR_ITEMS,
    CART_SAVE_SHIPPING_ADDRESS
} from '../constants/cartConstants'
import { ORDER_LIST_MY_RESET } from '../constants/orderConstants';

export const login = (email, password) => async (dispatch) => {
    try{
        dispatch({
            type: USER_LOGIN_REQUEST,
        });
        const config = {
            headers: {
                'Content-Type':'application/json'
            }
        }

        const {data} = await axios.post(
                '/api/users/login/',
                {
                    'username': email,
                    'password': password,
                },
                config,
            );

        dispatch({
            type: USER_LOGIN_SUCCESS,
            payload: data,
        });

        localStorage.setItem('userInfo', JSON.stringify(data))

    }catch(error){
        dispatch({
            type    : USER_LOGIN_FAIL,
            payload : error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,

        });
    }
}

export const logout = () => (dispatch) => {
    localStorage.removeItem('userInfo')
    localStorage.removeItem('cartItems')
    localStorage.removeItem('shippingAddress')
    dispatch({type: USER_LOGOUT})
    dispatch({type: USER_DETAILS_RESET})
    dispatch({type: USER_ADDRESS_DETAILS_RESET})
    dispatch({type: CART_CLEAR_ITEMS})
    dispatch({type: USER_LIST_RESET})
    dispatch({type: ORDER_LIST_MY_RESET})
}

export const register = (name, email, password) => async (dispatch) => {
    try{
        dispatch({
            type: USER_REGISTER_REQUEST,
        });
        const config = {
            headers: {
                'Content-Type':'application/json'
            }
        }

        const {data} = await axios.post(
                '/api/users/register/',
                {
                    'name': name,
                    'email': email,
                    'password': password,
                },
                config,
            )

        dispatch({
            type: USER_REGISTER_SUCCESS,
            payload: data,
        })

        dispatch({
            type: USER_LOGIN_SUCCESS,
            payload: data,
        })

        localStorage.setItem('userInfo', JSON.stringify(data));

    }catch(error){

        dispatch({
            type    : USER_REGISTER_FAIL,
            payload : error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,

        })
    }
}

export const getUserDetails = request => async (dispatch, getState) => {
    try{
        dispatch({
            type: USER_DETAILS_REQUEST,
        })

        const {
            userLogin:{ userInfo }
        } = getState()

        const config = {
            headers: {
                'Content-Type':'application/json',
                AUthorization: `Bearer ${userInfo.token}`,
            }
        }

        const {data} = await axios.get(
                `/api/users/${request}/`,
                config,
            )

        dispatch({
            type: USER_DETAILS_SUCCESS,
            payload: data,
        })

    }catch(error){
        dispatch({
            type    : USER_DETAILS_FAIL,
            payload : error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,

        })
    }
}

export const getUserAddressDetails = () => async (dispatch, getState) => {
    try{
        dispatch({
            type: USER_ADDRESS_DETAILS_REQUEST,
        })

        const {
            userLogin:{ userInfo }
        } = getState()

        const config = {
            headers: {
                'Content-Type':'application/json',
                AUthorization: `Bearer ${userInfo.token}`,
            }
        }

        const {data} = await axios.get(
                `/api/users/address/retrieve/`,
                config,
            )

        dispatch({
            type: USER_ADDRESS_DETAILS_SUCCESS,
            payload: data,
        })

        dispatch({
            type: CART_SAVE_SHIPPING_ADDRESS,
            payload: data,
        })

        localStorage.setItem('shippingAddress', JSON.stringify(data))

    }catch(error){
        dispatch({
            type    : USER_ADDRESS_DETAILS_FAIL,
            payload : error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,

        })
    }
}

export const saveUserAddress = userAddress => async (dispatch, getState) => {

    try{
        const { userLogin:{ userInfo }} = getState()

        const config = {
            headers: {
                'Content-Type':'application/json',
                AUthorization: `Bearer ${userInfo.token}`,
            }
        }

        const {data} = await axios.patch(
                `/api/users/address/update/`,
                {
                    'address': userAddress['address'],
                    'city': userAddress['city'],
                    'zipCode': userAddress['zipCode'],
                },
                config,
        )

        dispatch({
            type: USER_ADDRESS_DETAILS_SUCCESS,
            payload: data,
        })

        dispatch({
            type: CART_SAVE_SHIPPING_ADDRESS,
            payload: data,
        })

        localStorage.setItem('shippingAddress', JSON.stringify(data))

    }catch(error){

        dispatch({
                type : USER_ADDRESS_DETAILS_FAIL,
                payload : error.response && error.response.data.detail
                            ? error.response.data.detail
                            : error.message,
            })
    }
}

export const updateUserProfile = user => async (dispatch, getState) => {
    try{
        dispatch({
            type: USER_UPDATE_PROFILE_REQUEST,
        })

        const {
            userLogin:{ userInfo }
        } = getState()

        const config = {
            headers: {
                'Content-Type':'application/json',
                AUthorization: `Bearer ${userInfo.token}`,
            }
        }

        const {data} = await axios.put(
                `/api/users/details/update/`,
                user,
                config,
            )

        dispatch({
            type: USER_UPDATE_PROFILE_SUCCESS,
            payload: data,
        })

        dispatch({
            type: USER_LOGIN_SUCCESS,
            payload: data,
        })

        localStorage.setItem('userInfo', JSON.stringify(data));

    }catch(error){
        dispatch({
            type    : USER_UPDATE_PROFILE_FAIL,
            payload : error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,

        })
    }
}

export const listUsers = () => async (dispatch, getState) => {
    try{
        dispatch({
            type: USER_LIST_REQUEST,
        })

        const {
            userLogin:{ userInfo }
        } = getState()

        const config = {
            headers: {
                'Content-Type':'application/json',
                AUthorization: `Bearer ${userInfo.token}`,
            }
        }

        const {data} = await axios.get(
                `/api/users/admin/`,
                config,
            )

        dispatch({
            type: USER_LIST_SUCCESS,
            payload: data,
        })

    }catch(error){
        dispatch({
            type    : USER_LIST_FAIL,
            payload : error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,

        });
    }
}

export const deleteUser = id => async (dispatch, getState) => {
    try{
        dispatch({
            type: USER_DELETE_REQUEST,
        })

        const {
            userLogin:{ userInfo }
        } = getState()

        const config = {
            headers: {
                'Content-Type':'application/json',
                AUthorization: `Bearer ${userInfo.token}`,
            }
        }

        await axios.delete(
                `/api/users/admin/${id}/`,
                config,
            )

        dispatch({
            type: USER_DELETE_SUCCESS,
        })

    }catch(error){
        dispatch({
            type    : USER_DELETE_FAIL,
            payload : error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,

        });
    }
}

export const updateUser = user => async (dispatch, getState) => {
    try{
        dispatch({
            type: USER_UPDATE_REQUEST,
        })

        const {
            userLogin:{ userInfo }
        } = getState()

        const config = {
            headers: {
                'Content-Type':'application/json',
                AUthorization: `Bearer ${userInfo.token}`,
            }
        }

        const {data} = await axios.put(
                `/api/users/admin/${user.id}/`,
                user,
                config,
            )

        dispatch({
            type: USER_UPDATE_SUCCESS,
        })

        dispatch({
            type: USER_DETAILS_SUCCESS,
            payload: data,
        })

    }catch(error){
        dispatch({
            type    : USER_UPDATE_FAIL,
            payload : error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,

        });
    }
}