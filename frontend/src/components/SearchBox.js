import {useState} from 'react'
import{Button, Form} from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'

export default function SearchBox() {

    const navigate = useNavigate()

    const [keyword, SetKeyword] = useState('')

    const submitHandler = e => {
        e.preventDefault()
        if(keyword){
            navigate(`/keyword=${keyword}&page=1`)
        }
    }

    return (
        <Form onSubmit={submitHandler} className='d-flex me-5 p-2'>
            <Form.Control
                type='text'
                name='q'
                onChange={e => SetKeyword(e.target.value)}
                className='mr-sm-2 ml-sm-5'
            ></Form.Control>
            <Button
                type='submit'
                variant='outline-success'
                className='ms-2 btn-outline-light'
            >
                Submint
            </Button>
        </Form>
    )
}