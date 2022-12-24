import {useState, useEffect } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { Form, Button } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import FormContainer from '../components/FormContainer'
import { getUserDetails, updateUser } from '../actions/userActions'
import { USER_UPDATE_RESET } from '../constants/userConstants'

export default function UserEditScreen() {

    const {userId} = useParams()
    const navigate = useNavigate()

    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [isAdmin, setIsAdmin] = useState(false)
    const [password, setPassword] = useState('')

    const dispatch = useDispatch()

    const {
        loading,
        user,
        error
    } = useSelector(state => state.userDetails)
    const {
        loading: loadingUpdate,
        success: successUpdate,
        error: errorUpdate
    } = useSelector(state => state.userUpdate)

    useEffect(() => {

        if(!user || !Object.keys(user).length){
            navigate('/admin/userlist')
        }

        if(successUpdate){
            dispatch({type: USER_UPDATE_RESET})
            navigate('/admin/userlist')
        }else{
            if(!user.name || user.id !== Number(userId)){
                dispatch({type: USER_UPDATE_RESET})
                dispatch(getUserDetails(userId))
            }else{
                setName(user.name)
                setEmail(user.email)
                setIsAdmin(user.isAdmin)
            }
        }

    }, [user, userId, successUpdate])

    const submitHandler = e => {
        e.preventDefault()
        dispatch(updateUser({
            id:user.id,
            name,
            email,
            isAdmin,
            password,
        }))
    }

  return (
    <>
        <Link to='/admin/userlist' className='btn btn-light my-3 rounded boxshadow'>
            Go Back
        </Link>
        <FormContainer>
            <h1>Edit User</h1>
            {loadingUpdate && <Loader/>}
            {errorUpdate && <Message variant='danger'>{errorUpdate}</Message>}
            {loading
                ? <Loader/>
                : error
                    ? <Message variant='danger'>{error}</Message>
                    : (<Form onSubmit={submitHandler}>

                            <Form.Group controlId='name'>
                                <Form.Label>Name</Form.Label>
                                <Form.Control
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
                                    type='email'
                                    placeholder='Enter Email'
                                    value={email}
                                    onChange={e => setEmail(e.target.value)}
                                >
                                </Form.Control>
                            </Form.Group>

                            <Form.Group controlId='isAdmin' className='mt-2'>
                                <Form.Check
                                    type='checkbox'
                                    label='Is Admin'
                                    checked={isAdmin}
                                    onChange={e => setIsAdmin(e.target.checked)}
                                >
                                </Form.Check>
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

                            <Button
                                className='mt-2'
                                type='submit'
                                variant='primary'>
                                    Update
                            </Button>

                        </Form>
                    )}
        </FormContainer>
    </>
  )
}