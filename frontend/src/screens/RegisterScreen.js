import {useState, useEffect } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { Form, Button, Row, Col } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import FormContainer from '../components/FormContainer'
import { register } from '../actions/userActions'

export default function RegisterScreen() {

    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [message, setMessage] = useState('')

    const dispatch = useDispatch()

    let { redirect } = useParams()
    const navigate = useNavigate()

    const { error, loading, userInfo } = useSelector(state => state.userRegister)

    useEffect(() => {
      if(userInfo){
        navigate(`/${redirect? redirect: ''}`)
      }
    }, [userInfo, redirect])

    const submitHandler = e => {
        e.preventDefault()
        if(password != confirmPassword) 
            setMessage('Passwords do not match')
        else if(password.length < 8 && password.length)
            setMessage('Passwords must be at least 8 characters')
        else
            dispatch(register(name, email, password))
    }

  return (
    <FormContainer>
        <h1>Register</h1>
        {message && <Message variant='danger'>{message}</Message>}
        {error && <Message variant='danger'>{error}</Message>}
        {loading && <Loader/>}
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
                    required
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
                    required
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
                    Register
            </Button> 

        </Form>
        <Row className='py-3'>
            <Col>
                Have an Account? <Link to={redirect? `/login/${redirect}`: '/login'}>Sing In</Link>
            </Col>
        </Row>
    </FormContainer>
  )
}