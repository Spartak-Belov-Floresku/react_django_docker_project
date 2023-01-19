import { Pagination } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

export default function Paginate({ pages, page, keyword = '', isAdmin = false}){
    if(keyword){
        keyword = keyword.split('keyword=')[1].split('&')[0];
    }
    return (pages > 1 &&
        <Pagination>
            {[...Array(pages).keys()].map(p => (
                <LinkContainer
                    key={p + 1}
                    to={ !isAdmin
                            ? `/keyword=${keyword}&page=${p + 1}`
                            : `/admin/productlist/keyword=${keyword}&page=${p + 1}`
                        }
                >
                    <Pagination.Item active={p + 1 === page}>{p + 1}</Pagination.Item>
                </LinkContainer>
            ))}
        </Pagination>
    )
}