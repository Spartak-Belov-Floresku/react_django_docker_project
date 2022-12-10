import { createStore, applyMiddleware, combineReducers } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'
import {
    productListReducers,
    productDetailsReducer,
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

const reducer = combineReducers({
    productList: productListReducers,
    productDetails: productDetailsReducer,

    cart: cartRuducers,

    userLogin: userLoginReducers,
    userRegister: userRegisterReducers,
    userDetails: userDetailsReducers,
    userAddressDetails: userAddressDetailsReducers,
    userUpdateProfile: userUpdateProfileReducers,
    usersList: userListReducers,
    userDelete: userDeleteReducers,
    userUpdate: userUpdateReducers,
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