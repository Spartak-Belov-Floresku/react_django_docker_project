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

const reducer = combineReducers({
    productList: productListReducers,
    productDetails: productDetailsReducer,
    cart: cartRuducers,
})

const initialState = {
    cart: {
        cartItems: localStorage.getItem('cartItems')? JSON.parse(localStorage.getItem('cartItems')): [],
    }
}

const mmiddleware = [thunk]

const store = createStore(reducer, initialState, composeWithDevTools(applyMiddleware(...mmiddleware)))

export default store;