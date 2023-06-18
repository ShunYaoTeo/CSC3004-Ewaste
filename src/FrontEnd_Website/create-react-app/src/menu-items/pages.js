// assets
import { IconKey } from '@tabler/icons';
import { IconLetterE } from '@tabler/icons';
import { IconCrown } from '@tabler/icons';

// constant
const icons = {
  IconKey,
  IconLetterE,
  IconCrown
};

// ==============================|| EXTRA PAGES MENU ITEMS ||============================== //

const pages = {
  id: 'pages',
  title: 'Pages',
  caption: 'Pages Caption',
  type: 'group',
  children: [
    {
      id: 'authentication',
      title: 'Authentication',
      type: 'collapse',
      icon: icons.IconKey,

      children: [
        {
          id: 'login3',
          title: 'Login',
          type: 'item',
          url: '/pages/login/login3',
          target: true
        },
        {
          id: 'register3',
          title: 'Register',
          type: 'item',
          url: '/pages/register/register3',
          target: true
        }
      ]
    },
    {
      id: 'Ewaste',
      title: 'E-Waste',
      type: 'collapse',
      icon: icons.IconLetterE,
      
      children: [
        {
          id: 'AddEwaste',
          title: 'Add E-Waste',
          type: 'item',
          url: '/AddEwaste',
          target: false
        }
      ]
    },
    {
      id: 'Rewards',
      title: 'Rewards',
      type: 'collapse',
      icon: icons.IconCrown,
      
      children: [
        {
          id: 'Rewards',
          title: 'Rewards',
          type: 'item',
          url: '/Rewards',
          target: false
        }
      ]
    }
    
  ]
};

export default pages;
