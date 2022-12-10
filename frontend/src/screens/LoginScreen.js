import {useState, useEffect } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { Form, Button, Row, Col } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import FormContainer from '../components/FormContainer'
import { login } from '../actions/userActions'

export default function LoginScreen() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const dispatch = useDispatch()

    let { redirect } = useParams()
    const navigate = useNavigate()

    const {error, loading, userInfo } = useSelector(state => state.userLogin)

    useEffect(() => {

      if(userInfo)
        navigate(`/${redirect? redirect: ''}`)

    }, [userInfo, redirect])

    const submitHandler = e => {
      e.preventDefault()
      dispatch(login(email, password))
    }

  return (
    <FormContainer>
      <h1>Sing In</h1>
      {error && <Message variant='danger'>{error}</Message>}
      {loading && <Loader/>}
      <Form onSubmit={submitHandler}>
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
        <Button
          className='mt-2'
          type='submit'
          variant='primary'>
            Sing In
        </Button>
      </Form>
      <Row className='py-3'>
        <Col>
          New Customer? <Link to={redirect? `/register/${redirect}`: '/register'}>Register</Link>
        </Col>
      </Row>
    </FormContainer>
  )
}