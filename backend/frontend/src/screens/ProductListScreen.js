import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { LinkContainer } from 'react-router-bootstrap'
import { Table, Button, Row, Col } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import Paginate from '../components/Paginate'
import {
    getUserDetails,
    logout,
 } from '../actions/userActions'
 import {
    listProductsAdmin,
    deleteProduct,
    createProduct,
} from '../actions/productActions'
import {
    PRODUCT_DELETE_RESET,
    PRODUCT_CREATE_RESET,
} from '../constants/productConstants'

export default function ProductListScreen() {

    const [unactive, setUnactive] = useState(false)
    const navigate = useNavigate()
    const dispatch = useDispatch()

    const { loading, products, page, pages, error } = useSelector(state => state.productAdminList)
    const {
        loading: loadingDelete,
        success: successDelete,
        error: errorDelete
    } = useSelector(state => state.productDelete)
    const {
        loading: loadingCreate,
        success: successCreate,
        product: createdProduct,
        error: errorCreate
    } = useSelector(state => state.productCreate)
    const { userInfo } = useSelector(state => state.userLogin);
    const {
        user: userDetails,
        error: errorDetails
    } = useSelector(state => state.userDetails)

    useEffect(() => {

        dispatch({type: PRODUCT_CREATE_RESET})
        localStorage.getItem('unactive')? setUnactive(true): setUnactive(false)

        if(!userInfo || !userInfo.isAdmin){
            navigate('/login')
        }

        if(userInfo){
            if(typeof userDetails !== 'object' || !Object.keys(userDetails).length)
                dispatch(getUserDetails('details/profile'))
            if(errorDetails == 'Given token not valid for any token type'){
                dispatch(logout())
            }
        }

        if(successCreate){
            navigate(`/admin/product/${createdProduct.id}/edit`)
        } else {
            dispatch(listProductsAdmin())
        }

    },[dispatch, userInfo, userDetails, successDelete, successCreate ])

    const deleteHandler = id => {
        if(window.confirm(`Are you sure? You want to delete this product ${id}`)){
            dispatch(deleteProduct(id))
        }
        dispatch({type: PRODUCT_DELETE_RESET})
    }

    const createProductHandler = () => {
        dispatch(createProduct())
    }

    const getUnactiveProducts = () => {

        ! localStorage.getItem('unactive')
            ? localStorage.setItem('unactive', true)
            : localStorage.removeItem('unactive')

        localStorage.getItem('unactive')
            ? setUnactive(true)
            : setUnactive(false)

        dispatch(listProductsAdmin())
    }

    return (
        <>
            <Row className='align-items-center'>
                <Col>
                    <h2>Products</h2>
                </Col>
                <Col className='text-end'>
                    <Button className='my-3 m-3' onClick={getUnactiveProducts}>
                        <i className={unactive? 'fas fa-plus':'fas fa-minus'}></i> Unactive Products
                    </Button>
                    <Button className='my-3' onClick={createProductHandler}>
                        <i className='fas fa-plus'></i> Create Product
                    </Button>
                </Col>
            </Row>

            {loadingDelete && <Loader/>}
            {errorDelete && <Message variant='danager'>{errorDelete}</Message>}

            {loadingCreate && <Loader/>}
            {errorCreate && <Message variant='danager'>{errorCreate}</Message>}

            {loading
                ? <Loader />
                : error
                    ? <Message variant='danger'>{error}</Message>
                    : (
                        <div>
                            <Table striped bordered hover responsive className='table-sm opacity'>
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>NAME</th>
                                        <th>PRICE</th>
                                        <th>CATEGORY</th>
                                        <th>BRAND</th>
                                        <th></th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {products && products.map(product => (
                                                <tr key={product.id}>
                                                    <td>{product.id}</td>
                                                    <td>{product.name}</td>
                                                    <td>${product.price}</td>
                                                    <td>{product.category}</td>
                                                    <td>{product.brand}</td>
                                                    <td>
                                                        <LinkContainer to={`/admin/product/${product.id}/edit`} className='me-2'>
                                                            <Button variant='light' className='btn-sm'>
                                                                <i className='fas fa-edit'></i>
                                                            </Button>
                                                        </LinkContainer>
                                                        <Button
                                                            variant='danger'
                                                            className='btn-sm'
                                                            onClick={() => deleteHandler(product.id)}>
                                                            <i className='fas fa-trash'></i>
                                                        </Button>
                                                    </td>
                                                </tr>
                                    ))}
                                </tbody>
                            </Table>
                            <Paginate pages={pages} page={page} isAdmin={true}/>
                        </div>
                    )}
        </>
    )
}