import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { LinkContainer } from 'react-router-bootstrap'
import { Table, Button } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import { listOrders } from '../actions/orderActions'

export default function OrderListSreen() {

    const navigate = useNavigate()
    const dispatch = useDispatch()

    const { loading, orders, error } = useSelector(state => state.orderList)
    const { userInfo } = useSelector(state => state.userLogin);

    useEffect(() => {

        if(userInfo && userInfo.isAdmin){
            dispatch(listOrders())
        }else{
            navigate('/login')
        }

    },[dispatch, userInfo])

    return (
        <>
            <h2>Orders</h2>
            {loading
                ? <Loader />
                : error 
                    ? <Message variant='danger'>{error}</Message>
                    : (
                        <Table striped bordered hover responsive className='table-sm'>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>USER</th>
                                    <th>DATE</th>
                                    <th>TOTAL</th>
                                    <th>PIAD</th>
                                    <th>DELIVERED</th>
                                    <th></th>
                                </tr>
                            </thead>

                            <tbody>
                                {orders && orders.map(order => (
                                        <tr key={order.id}>
                                                <td>{order.id}</td>
                                                <td>{order.user && order.user.name}</td>
                                                <td>{order.createdAt.substring(0,10)}</td>
                                                <td>${order.totalPrice}</td>
                                                <td>{order.isPaid 
                                                        ? order.paidAt.substring(0,10)
                                                        : (<i className='fas fa-times' style={{color: 'red'}}></i>)
                                                }</td>
                                                <td>{order.isDelivered 
                                                        ? order.deliveredAt.substring(0,10)
                                                        : (<i className='fas fa-times' style={{color: 'red'}}></i>)
                                                }</td>
                                                <td>
                                                    <LinkContainer to={`/order/${order.id}`} className='me-2'>
                                                        <Button variant='light' className='btn-sm'>
                                                            Details
                                                        </Button>
                                                    </LinkContainer>
                                                </td>
                                            </tr>
                                ))}
                            </tbody>
                        </Table>
                    )}
        </>
    )
}