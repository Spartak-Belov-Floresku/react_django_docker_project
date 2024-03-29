import axios from 'axios'
import {
    PRODUCT_LIST_REQUEST,
    PRODUCT_LIST_SUCCESS,
    PRODUCT_LIST_FAIL,

    PRODUCT_ADMIN_LIST_REQUEST,
    PRODUCT_ADMIN_LIST_SUCCESS,
    PRODUCT_ADMIN_LIST_FAIL,

    PRODUCT_DETAILS_REQUEST,
    PRODUCT_DETAILS_SUCCESS,
    PRODUCT_DETAILS_FAIL,

    PRODUCT_DELETE_REQUEST,
    PRODUCT_DELETE_SUCCESS,
    PRODUCT_DELETE_FAIL,

    PRODUCT_CREATE_REQUEST,
    PRODUCT_CREATE_SUCCESS,
    PRODUCT_CREATE_FAIL,

    PRODUCT_UPDATE_REQUEST,
    PRODUCT_UPDATE_SUCCESS,
    PRODUCT_UPDATE_FAIL,

    PRODUCT_IMAGE_UPLOAD_REQUEST,
    PRODUCT_IMAGE_UPLOAD_SUCCESS,
    PRODUCT_IMAGE_UPLOAD_FAIL,

    PRODUCT_CREATE_REVIEW_REQUEST,
    PRODUCT_CREATE_REVIEW_SUCCESS,
    PRODUCT_CREATE_REVIEW_FAIL,

    PRODUCT_TOP_REQUEST,
    PRODUCT_TOP_SUCCESS,
    PRODUCT_TOP_FAIL,
} from '../constants/productConstants'

export const listProducts = (keyword='') => async (dispatch) => {

    const arr_keywords = keyword.split("/")

    const query = arr_keywords[1] !== 'undefined'? `${arr_keywords[0]}/?${arr_keywords[1]}`: arr_keywords[0]+'/';

    try{
        dispatch({
            type: PRODUCT_LIST_REQUEST,
        })
        const {data} = await axios.get(`/api/products/${query}`)
        dispatch({
            type: PRODUCT_LIST_SUCCESS,
            payload: data,
        })

    }catch(error){
        dispatch({
            type: PRODUCT_LIST_FAIL,
            payload: error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,
        })
    }
}

export const listProductsAdmin = () => async (dispatch, getState) => {
    try{
        dispatch({
            type: PRODUCT_ADMIN_LIST_REQUEST,
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

        const unactive = localStorage.getItem('unactive')? '?unactive=True': '/'

        const {data} = await axios.get(
                `/api/products/admin${unactive}`,
                config,
            )
        dispatch({
            type: PRODUCT_ADMIN_LIST_SUCCESS,
            payload: data,
        })

    }catch(error){
        dispatch({
            type: PRODUCT_ADMIN_LIST_FAIL,
            payload: error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,
        })
    }
}


export const listTopProducts = () => async (dispatch) => {


    try{
        dispatch({type: PRODUCT_TOP_REQUEST});

        const { data } = await axios.get(`/api/products/user/top/`);

        dispatch({
            type: PRODUCT_TOP_SUCCESS,
            payload: data,
        });
    }catch(error){
        dispatch({
            type: PRODUCT_TOP_FAIL,
            payload: error.response && error.response.data.detail
                ? error.response.data.detail
                : error.message,
        })
    }
}


export const listProductDetails = id => async (dispatch) => {
    try{
        dispatch({
            type: PRODUCT_DETAILS_REQUEST,
        })
        const {data} = await axios.get(`/api/products/user/${id}/`)
        dispatch({
            type: PRODUCT_DETAILS_SUCCESS,
            payload: data,
        })

    }catch(error){
        dispatch({
            type: PRODUCT_DETAILS_FAIL,
            payload: error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,
        })
    }
}


export const deleteProduct = id => async (dispatch, getState) => {
    try{
        dispatch({
            type: PRODUCT_DELETE_REQUEST,
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
                `/api/products/admin/${id}/`,
                config,
            )

        dispatch({
            type: PRODUCT_DELETE_SUCCESS,
        })
    }catch(error){
        dispatch({
            type : PRODUCT_DELETE_FAIL,
            payload : error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,

        })
    }
}


export const createProduct = () => async (dispatch, getState) => {
    try{
        dispatch({
            type: PRODUCT_CREATE_REQUEST,
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

            const { data } = await axios.post(
                `/api/products/admin/`,
                {},
                config,
            );

        dispatch({
            type: PRODUCT_CREATE_SUCCESS,
            payload: data,
        })
    }catch(error){
        dispatch({
            type : PRODUCT_CREATE_FAIL,
            payload : error.response && error.response.data.detail
                        ? error.response.data.detail
                        : error.message,

        });
    }
}

export const updateProduct = product => async (dispatch, getState) => {
    try{
        dispatch({
            type: PRODUCT_UPDATE_REQUEST
        });

        const {
            userLogin: {userInfo},
        } = getState()

        const config = {
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userInfo.token}`,
            }
        }

        const {data} = await axios.put(
            `/api/products/admin/${product.id}/`,
            product,
            config
        );

        dispatch({
            type: PRODUCT_UPDATE_SUCCESS,
            payload: data
        });

        dispatch({
            type: PRODUCT_DETAILS_SUCCESS,
            payload: data,
        });

    }catch(error){
        dispatch({
            type: PRODUCT_UPDATE_FAIL,
            payload: error.response && error.response.data.detail
                ? error.response.data.detail
                : error.message,
        })
    }
}

export const uploadProductImage = formData => async (dispatch, getState) => {
    try{

        dispatch({
            type: PRODUCT_IMAGE_UPLOAD_REQUEST
        });

        const {
            userLogin: {userInfo},
        } = getState()

        const config = {
            headers: {
                'Content-Type': 'multipart/form-data',
                Authorization: `Bearer ${userInfo.token}`,
            }
        }

        const {data} = await axios.post(
            '/api/products/admin/image/',
            formData,
            config,
        );

        dispatch({
            type: PRODUCT_IMAGE_UPLOAD_SUCCESS,
            payload: data
        });

    }catch(error){
        dispatch({
            type: PRODUCT_IMAGE_UPLOAD_FAIL,
            payload: error.response && error.response.data.detail
                ? error.response.data.detail
                : error.message,
        })
    }
}

export const createProductReview = (productId, review) => async (dispatch, getState) => {
    try{
        dispatch({
            type: PRODUCT_CREATE_REVIEW_REQUEST
        });

        const {
            userLogin: {userInfo},
        } = getState()

        const config = {
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${userInfo.token}`,
            }
        }

        const {data} = await axios.patch(
            `/api/products/user/reviews/${productId}/`,
            review,
            config
        );

        dispatch({
            type: PRODUCT_CREATE_REVIEW_SUCCESS,
            payload: data
        });

    }catch(error){
        dispatch({
            type: PRODUCT_CREATE_REVIEW_FAIL,
            payload: error.response && error.response.data.detail
                ? error.response.data.detail
                : error.message,
        })
    }
}