import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { LinkContainer } from 'react-router-bootstrap'
import { Table, Button } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import { listUsers, deleteUser } from '../actions/userActions'

export default function UserListSreen() {

    const navigate = useNavigate()
    const dispatch = useDispatch()

    const { loading, users, error } = useSelector(state => state.usersList)
    const { userInfo } = useSelector(state => state.userLogin);
    const { success: successDelete, error: errorDelete } = useSelector(state => state.userDelete);


    useEffect(() => {

        if(userInfo && userInfo.isAdmin){
            dispatch(listUsers())
        }else{
            navigate('/login')
        }

    },[dispatch, userInfo, successDelete])

    const deleteHandler = id => {
        if(window.confirm(`Are you sure? You want to delete this user ${id}`))
            dispatch(deleteUser(id))
    }

    return (
        <>
            <h2>Users</h2>
            {errorDelete && <Message variant='danger'>{errorDelete}</Message>}
            {loading
                ? <Loader />
                : error
                    ? <Message variant='danger'>{error}</Message>
                    : (
                        <Table striped bordered hover responsive className='table-sm'>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>NAME</th>
                                    <th>EMAIL</th>
                                    <th>ADMIN</th>
                                    <th></th>
                                </tr>
                            </thead>

                            <tbody>
                                {users && users.map(user => (
                                            <tr key={user.id}>
                                                <td>{user.id}</td>
                                                <td>{user.name}</td>
                                                <td>{user.email}</td>
                                                <td>{user.isAdmin
                                                        ? (<i className='fas fa-check' style={{color:'green'}}></i>)
                                                        : (<i className='fas fa-times' style={{color: 'red'}}></i>)
                                                }</td>
                                                <td>
                                                    <LinkContainer to={`/admin/user/${user.id}/edit`} className='me-2'>
                                                        <Button variant='light' className='btn-sm'>
                                                            <i className='fas fa-edit'></i>
                                                        </Button>
                                                    </LinkContainer>
                                                    <Button variant='danger' className='btn-sm' onClick={() => deleteHandler(user.id)}>
                                                        <i className='fas fa-trash'></i>
                                                    </Button>
                                                </td>
                                            </tr>
                                ))}
                            </tbody>
                        </Table>
                    )}
        </>
    )
}