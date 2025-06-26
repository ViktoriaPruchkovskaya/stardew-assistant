import { useNavigate } from 'react-router';
//@ts-ignore
import image from 'url:../assets/stardew-valley-assistant.png';

export default function Header() {
    const navigate = useNavigate()
    const handleOnClick = () => {
        navigate('/')
    }
    return <div>
        <img
            src={image}
            className="w-lg mx-auto drop-shadow-lg cursor-pointer"
            onClick={handleOnClick}
        />
    </div>
}