import { createStore, applyMiddleware, combineReducers } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'
import {
    productListReducer,
    productAdminListReducer,
    productDetailsReducer,
    productDeleteReducer,
    productCreateReducer,
    productUpdateReducer,
    productImageUploadReducer,
    productReviewCreateReducer,
    productTopRatedReducer,
} from './reducers/productReducers'
import {
    cartRuducers,
} from './reducers/cartReducers'
import {
    userLoginReducers,
    userRegisterReducers,
    userDetailsReducers,
    userAddressDetailsReducers,
    userUpdateProfileReducers,
    userListReducers,
    userDeleteReducers,
    userUpdateReducers,
} from './reducers/userReducers'
import {
    orderCreateReducer,
    orderDetailsReducer,
    orderPayReducer,
    orderListMyReducer,
    orderListReducer,
    orderDeliverReducer,
} from './reducers/orderReducers'

const reducer = combineReducers({
    productList: productListReducer,
    productAdminList: productAdminListReducer,
    productDetails: productDetailsReducer,
    productDelete: productDeleteReducer,
    productCreate: productCreateReducer,
    productUpdate: productUpdateReducer,
    productImageUpload: productImageUploadReducer,
    productReviewCreate: productReviewCreateReducer,
    productTopRated: productTopRatedReducer,

    cart: cartRuducers,

    userLogin: userLoginReducers,
    userRegister: userRegisterReducers,
    userDetails: userDetailsReducers,
    userAddressDetails: userAddressDetailsReducers,
    userUpdateProfile: userUpdateProfileReducers,
    usersList: userListReducers,
    userDelete: userDeleteReducers,
    userUpdate: userUpdateReducers,

    orderCreate: orderCreateReducer,
    orderDetails: orderDetailsReducer,
    orderPay: orderPayReducer,
    orderListMy: orderListMyReducer,
    orderList: orderListReducer,
    orderDeliver: orderDeliverReducer,
})

const initialState = {
    cart: {
        cartItems: localStorage.getItem('cartItems')? JSON.parse(localStorage.getItem('cartItems')): [],
        shippingAddress: localStorage.getItem('shippingAddress')? JSON.parse(localStorage.getItem('shippingAddress')): {},
    },
    userLogin: {userInfo: localStorage.getItem('userInfo')? JSON.parse(localStorage.getItem('userInfo')): null},
}

const mmiddleware = [thunk]

const store = createStore(reducer, initialState, composeWithDevTools(applyMiddleware(...mmiddleware)))

export default store;