import React from 'react';

import { VerticalNavLabel } from './VerticalNavLabel';
import { VerticalNavItem } from './NavItem';
import { ExpansionPanel } from './ExpansionPanel';
import { useMenuSliceSelector } from '../slice';

export const VerticalNav = ({ sidebarMode }) => {
    const items = useMenuSliceSelector((state) => state.navigations);

    const renderLevels = (data) =>
        data.map((item, index) => {
            if (item.type === 'label')
                return <VerticalNavLabel key={index} sidebarMode={sidebarMode} label={item.label} />;
            if (item.children) {
                return (
                    <ExpansionPanel mode={sidebarMode} item={item} key={index}>
                        {renderLevels(item.children)}
                    </ExpansionPanel>
                );
            }
            return <VerticalNavItem key={index} sidebarMode={sidebarMode} item={item} />;
        });

    return <div>{renderLevels(items)}</div>;
};
