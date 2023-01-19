import Spinner from 'react-bootstrap/Spinner'

export default function Loader() {
    return (
        <Spinner
            animation="border"
            role="status"
            style={{
                width: '180px',
                height: '180px',
                margin: '5em auto 0',
                display: 'block'
            }}
        >
          <span className="visually-hidden">Loading...</span>
        </Spinner>
    );
}