import {useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Form, Button, Row, Col, Table } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import { getUserDetails, updateUserProfile, logout } from '../actions/userActions'
import { USER_UPDATE_PROFILE_RESET } from '../constants/userConstants'
import { listMyOrders } from '../actions/orderActions'

export default function ProfileScreen() {

    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [message, setMessage] = useState('')
    const navigate = useNavigate()

    const dispatch = useDispatch()

    const { loading: loadingProfile, user: userProfile, error: errorProfile } = useSelector(state => state.userDetails)
    const { userInfo } = useSelector(state => state.userLogin)
    const { success } = useSelector(state => state.userUpdateProfile)
    const { loading: loadingOrders, orders: listOrders, error: errorOrders } = useSelector(state => state.orderListMy)

    useEffect(() => {
        if(!userInfo){
            navigate(`/login`)
        }else{
            if(!userProfile || !userProfile.name || success || userInfo.id !== userProfile.id){
                dispatch({type: USER_UPDATE_PROFILE_RESET})
                dispatch(getUserDetails('profile'))
                dispatch(listMyOrders())
                setPassword('')
                setConfirmPassword('')
            }else{
                setName(userProfile.name)
                setEmail(userProfile.email)
            }
        }

        if(errorProfile == 'Given token not valid for any token type')
            dispatch(logout())

    }, [dispatch, navigate, userInfo, userProfile, success])

    const submitHandler = e => {
        e.preventDefault()
        if(password != confirmPassword){
            setMessage('Passwords do not match')
        }else if(password.length < 8 && password.length){
            setMessage('Passwords must be at least 8 characters')
        }else{
            dispatch(updateUserProfile({
                'id': userProfile.id,
                'name': name,
                'email': email,
                'password': password,
            }))
            setMessage('');
            setPassword('');
            setConfirmPassword('');
        }
    }

  return (
    <Row>
        <Col md={3}>
            <h2>User Profile</h2>
            {message && <Message variant='danger'>{message}</Message>}
            {errorProfile && <Message variant='danger'>{errorProfile}</Message>}
            {loadingProfile && <Loader/>}
            <Form onSubmit={submitHandler}>

                <Form.Group controlId='name'>
                    <Form.Label>Name</Form.Label>
                    <Form.Control
                        required
                        type='name'
                        placeholder='Enter name'
                        value={name}
                        onChange={e => setName(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId='email'>
                    <Form.Label>Email Address</Form.Label>
                    <Form.Control
                        required
                        type='email'
                        placeholder='Enter Email'
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId='password'>
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type='password'
                        placeholder='Enter Password'
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>

                <Form.Group controlId='confirmPassword'>
                    <Form.Label>Confirm Password</Form.Label>
                    <Form.Control
                        type='password'
                        placeholder='Confirm Password'
                        value={confirmPassword}
                        onChange={e => setConfirmPassword(e.target.value)}
                    >
                    </Form.Control>
                </Form.Group>

                <Button
                    className='mt-2'
                    type='submit'
                    variant='primary'>
                        Update
                </Button>

            </Form>
        </Col>
        <Col md={9}>
            <h2>My Orders</h2>
            {loadingOrders ? (
                <Loader/>
            ) : errorOrders ? (
                <Message variant='danger'>{errorOrders}</Message>
            ) : (
                <Table striped responsive className='table-sm'>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Date</th>
                            <th>Total</th>
                            <th>Paid</th>
                            <th>Delivered</th>
                        </tr>
                    </thead>
                    <tbody>
                        {listOrders.map(order => (
                            <tr key={order.id}>
                                <td>{order.id}</td>
                                <td>{order.createdAt.substring(0,10)}</td>
                                <td>${order.totalPrice}</td>
                                <td>{order.isPaid? order.paidAt.substring(0,10) : (
                                    <i className='fas fa-times' style={{color: 'red'}}></i>
                                )}</td>
                                <td>
                                    <LinkContainer to={`/order/${order.id}`}>
                                        <Button className='btn-sm'>Details</Button>
                                    </LinkContainer>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            )}
        </Col>
    </Row>
  )
}