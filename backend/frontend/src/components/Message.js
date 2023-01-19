import Alert from 'react-bootstrap/Alert'

export default function Message({variant, children}) {
  return (
    <Alert variant={variant} className='text-center'>
      {children}
    </Alert>
  )
}