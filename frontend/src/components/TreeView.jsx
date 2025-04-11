import React from 'react';

import Collapse from '@mui/material/Collapse';
import {ExpandMore, ExpandLess, Done, Close} from "@mui/icons-material";
import TreeItem from '@mui/lab/TreeItem';
import TreeView from '@mui/lab/TreeView';
import {useSpring, animated} from 'react-spring';
import {Box, CircularProgress} from "@mui/material";
import _ from "lodash";

function TransitionComponent(props) {
  const style = useSpring({
    from: {opacity: 0, transform: 'translate3d(20px,0,0)'},
    to: {opacity: props.in ? 1 : 0, transform: `translate3d(${props.in ? 0 : 20}px,0,0)`},
  });

  return (<animated.div style={style}>
    <Collapse {...props} />
  </animated.div>);
}


const EndTreeItemMemo = ({nodeId, label, status}) => {
  const Icon = ({status}) => {
    switch (status) {
      case 'success':
        return <Done
          sx={{
            color: '#08ad6c'
          }}
          style={{fontSize: "1.5rem"}}
        />;
      case 'fail':
        return <Close
          sx={{
            color: 'error.main'
          }}
          style={{fontSize: "1.5rem"}}
        />;
      case 'pending':
        return (<Box display="flex" alignItems="center" height={24} width={24}>
          <CircularProgress size={18} sx={{color: 'primary.main'}}/>
        </Box>);
      default:
        return (<Done/>);
    }
  }

  return (<TreeItem
    nodeId={nodeId}
    label={label}
    endIcon={<Icon status={status}/>}
  />)
}

const EndTreeItem = React.memo(EndTreeItemMemo)

function calcDefaultExpanded(nodes) {
  const result = []
  const addNodeToExpanded = (nodes, nestingLevel, parent) => {
    nodes.forEach((node, index) => {
      const nodeName = `${parent}:::${node.name}[${index}]`
      if (nestingLevel < 3) {
        result.push(nodeName)
        if (Array.isArray(node.inner)) {
          addNodeToExpanded(node.inner, nestingLevel + 1, nodeName)
        }
      }
    })
  }
  addNodeToExpanded(nodes, 0, 'root')
  return result
}

const CustomTreeViewMemo = ({steps}) => {
  const [expanded, setExpanded] = React.useState(calcDefaultExpanded(steps));

  const handleToggle = (event, nodeIds) => {
    setExpanded(nodeIds);
  };

  const renderTree = (nodes, nestingLevel, parent) => {
    return nodes.map((node, index) => {
      const nodeName = `${parent}:::${node.name}[${index}]`
      return (_.isEmpty(node.inner) ? <EndTreeItem
        key={nodeName}
        nodeId={nodeName}
        label={node.name}
        status={node.status}
      /> : <TreeItem
        sx={{
          '& .MuiTreeItem-group': {
            marginLeft: "15px !important", paddingLeft: "7px !important", borderLeft: `1px dashed`
          }, '& .MuiTreeItem-iconContainer': {
            '& .close': {
              opacity: 0.3,
            }
          }
        }}
        key={nodeName}
        nodeId={nodeName}
        label={node.name}
        TransitionComponent={TransitionComponent}
        expandIcon={<ExpandMore
          sx={[node.status === 'success' && {color: '#08ad6c'}, node.status === 'fail' && {color: 'error.main'}]}
          style={{fontSize: "1.5rem"}}
        />}
        collapseIcon={<ExpandLess
          sx={[node.status === 'success' && {color: '#08ad6c'}, node.status === 'fail' && {color: 'error.main'}]}
          style={{fontSize: "1.5rem"}}
        />}
      >
        {renderTree(node.inner, nestingLevel + 1, nodeName)}
      </TreeItem>)
    })
  };

  return (<TreeView
    expanded={expanded}
    onNodeToggle={handleToggle}
  >
    {renderTree(steps, 0, 'root')}
  </TreeView>);
}

export const CustomTreeView = React.memo(CustomTreeViewMemo);
