import {useEffect, useState} from 'react';
import axios from 'axios';
import {Link, useParams, useNavigate} from 'react-router-dom';
import {Form, Button,} from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import Loader from '../components/Loader';
import Message from '../components/Message';
import FormContainer from '../components/FormContainer';
import {
    listProductDetails,
    updateProduct,
    uploadProductImage,
} from '../actions/productActions';
import { PRODUCT_UPDATE_RESET } from '../constants/productConstants';

export const ProductEditScreen = () => {

    const { productId } = useParams();

    const dispatch = useDispatch();
    const navigate = useNavigate();

    const [name, setName] = useState('');
    const [price, setPrice] = useState(0);
    const [image, setImage] = useState('');
    const [brand, setBrand] = useState('');
    const [category, setCategory] = useState('');
    const [countInStock, setCountInStock] = useState(0);
    const [description, setDescription] = useState('');
    const [active, setActive] = useState(false);

    const productDetails = useSelector(state => state.productDetails);
    const {error, loading, product} = productDetails;

    const productUpdate = useSelector(state => state.productUpdate);
    const {error: errorUpdate, loading: loadingUpdate, success: successUpdate} = productUpdate;

    const productImageUpload = useSelector(state => state.productImageUpload);
    const {error: errorImage, loading: loadingImage, success: successImage} = productImageUpload;

    useEffect(()=>{

        if(successUpdate){
            dispatch({type: PRODUCT_UPDATE_RESET});
            navigate('/admin/productlist');
        }else{

            if(!product.name || product.id !== Number(productId)){
                dispatch(listProductDetails(productId));
            }else{
                setName(product.name)
                setPrice(product.price)
                setImage(product.image)
                setBrand(product.brand)
                setCategory(product.category)
                setCountInStock(product.countInStock)
                setDescription(product.description)
                setActive(product.active)
            }
        }

        if(successImage){
            setImage(successImage);
        }

    },[ dispatch, navigate, product, productId, successUpdate, successImage ])

    const submitHandler = (e) => {
        e.preventDefault();
        dispatch(updateProduct({
            id: product.id,
            name,
            price,
            image,
            brand,
            category,
            countInStock,
            description,
            active,
        }));
    }

    const uploadFileHandler = async (e) => {
        const file = e.target.files[0]
        const formData = new FormData()
        formData.append('image', file)
        formData.append('product_id', productId)
        dispatch(uploadProductImage(formData))
    }

    return (
        <>
        <Link to='/admin/productlist' className='btn btn-light my-3 rounded boxshadow'>
            Go Back
        </Link>

        <FormContainer>
            <h1>Edit Product:</h1>
            {loadingUpdate && <Loader/>}
            {errorUpdate && <Message variant='danger'>{errorUpdate}</Message>}

            { loading
                ? <Loader/>
                : error
                    ?   <Message variant='danger'>{error}</Message>
                    :   <Form onSubmit={submitHandler}>

                            <Form.Group controlId='name'>
                                <Form.Label>Name:</Form.Label>
                                <Form.Control
                                    type='name'
                                    placeholder='Enter name'
                                    value={name}
                                    onChange={e=> setName(e.target.value)}
                                >
                                </Form.Control>
                            </Form.Group>

                            <Form.Group controlId='price'>
                                <Form.Label>Price:</Form.Label>
                                <Form.Control
                                    type='number'
                                    placeholder='Enter price'
                                    value={price}
                                    onChange={e=> setPrice(e.target.value)}
                                >
                                </Form.Control>
                            </Form.Group>

                            <Form.Group controlId='image'>
                                <Form.Label>Image</Form.Label>
                                <Form.Control
                                    type='text'
                                    placeholder='Enter image'
                                    value={image? image: 'None'}
                                    onChange={e => setImage(e.target.value)}
                                >
                                </Form.Control>

                                <Form.Group controlId="formFile" className="mb-3">
                                    <Form.Control type="file" onChange={uploadFileHandler} />
                                </Form.Group>
                                {loadingImage && <Loader/>}
                                {errorImage && <Message variant='danger'>{errorImage}</Message>}
                            </Form.Group>

                            <Form.Group controlId='brand'>
                                <Form.Label>Brand:</Form.Label>
                                <Form.Control
                                    type='text'
                                    placeholder='Enter brand'
                                    value={brand}
                                    onChange={e=> setBrand(e.target.value)}
                                >
                                </Form.Control>
                            </Form.Group>

                            <Form.Group controlId='countinstock'>
                                <Form.Label>Stock:</Form.Label>
                                <Form.Control
                                    type='number'
                                    placeholder='Enter stock'
                                    value={countInStock}
                                    onChange={e=> setCountInStock(e.target.value)}
                                >
                                </Form.Control>
                            </Form.Group>

                            <Form.Group controlId='category'>
                                <Form.Label>Category:</Form.Label>
                                <Form.Control
                                    type='text'
                                    placeholder='Enter category'
                                    value={category}
                                    onChange={e=> setCategory(e.target.value)}
                                >
                                </Form.Control>
                            </Form.Group>

                            <Form.Group controlId='Description'>
                                <Form.Label>Description:</Form.Label>
                                <Form.Control
                                    type='text'
                                    placeholder='Enter Description'
                                    value={description}
                                    onChange={e=> setDescription(e.target.value)}
                                >
                                </Form.Control>
                            </Form.Group>

                            <Form.Group controlId='isActive' className='mt-2'>
                                <Form.Check
                                    type='checkbox'
                                    label='Is Active'
                                    checked={active}
                                    onChange={e => setActive(e.target.checked)}
                                >
                                </Form.Check>
                            </Form.Group>

                            <Button className='mt-3' type='submit' variant='primary'>Update</Button>
                        </Form>
            }
        </FormContainer>
        </>
    )
}