import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";

import Header from "../../components/Header";

import StatBox from "../../components/StatBox";

import { apidata } from "../../data/mockData";

import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import BatterySaverIcon from '@mui/icons-material/BatterySaver';


function createData(name, score, acc, val_acc) {
  return { name, score, acc, val_acc };
}
const Prediction = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const rows = [
    createData('Linear Regression', 0.65, 268, 274),
    createData('Random Forest', 0.96, 84, 87),
    createData('Neural Network', 0.88, 152, 153),
  ];
  const fontsize = 20;

  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="Prediction" subtitle="Battery Evaluation and Comparison with AI" />

        
      </Box>
      <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
        <TableHead>
          <TableRow>
            <TableCell sx={{fontSize:fontsize}}>Model Type</TableCell>
            <TableCell sx={{fontSize:fontsize}} align="right">R Score</TableCell>
            <TableCell sx={{fontSize:fontsize}} align="right">Train Error</TableCell>
            <TableCell sx={{fontSize:fontsize}} align="right">Test Error</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell sx={{fontSize:fontsize}} component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell sx={{fontSize:fontsize}} align="right">{row.score}</TableCell>
              <TableCell sx={{fontSize:fontsize}} align="right">{row.acc}</TableCell>
              <TableCell sx={{fontSize:fontsize}} align="right">{row.val_acc}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
      
      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="190px"
        gap="20px"
      >
        {/* ROW 1 */} 
        <Box
          gridColumn="span 4"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
        {apidata.map((data) => (
          <StatBox
            title={`1253/1434`}
            subtitle="Current Cycle/Total Cycle"
            progress = {1253/1434}
          />
          ))}
        </Box>
        <Box
          gridColumn="span 4"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
        <Box width="100%" m="0 30px">
          <Box display="flex" justifyContent="space-between">
            <Box>
              <Typography
                variant="h4"z
                fontWeight="bold"
                sx={{ color: colors.grey[100] }}
              >
                Require Replacement
              </Typography>
            </Box>
            <Box>
              <BatterySaverIcon style={{fontSize: '40px', color : "red"}}></BatterySaverIcon>
            </Box>
          </Box>
          <Box display="flex" justifyContent="space-between" mt="2px">
            <Typography variant="h5" sx={{ color: colors.greenAccent[500] }}>
              Condition
            </Typography>
            <Typography
              variant="h5"
              fontStyle="italic"
              sx={{ color: colors.greenAccent[600] }}
            >
              {/* {increase} */}
            </Typography>
          </Box>
        </Box>
        </Box>
        
        
        <Box
          gridColumn="span 4"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
        {apidata.map((data) => (
          <StatBox
            title={'24 Days'}
            subtitle="Remaining Time"
            progress={1253/1434}
          />
          ))}
        </Box>  

        {/* ROW 2 */}
        

        {/* ROW 3 */}
        {/* <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          p="30px"
        >
          <Typography variant="h5" fontWeight="600">
            Campaign
          </Typography>
          <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            mt="25px"
          >
            <ProgressCircle size="125" />
            <Typography
              variant="h5"
              color={colors.greenAccent[500]}
              sx={{ mt: "15px" }}
            >
              $48,352 revenue generated
            </Typography>
            <Typography>Includes extra misc expenditures and costs</Typography>
          </Box>
        </Box>
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ padding: "30px 30px 0 30px" }}
          >
            Sales Quantity
          </Typography>
          <Box height="250px" mt="-20px">
            <BarChart isDashboard={true} />
          </Box>
        </Box>
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          padding="30px"
        >
          <Typography
            variant="h5"
            fontWeight="600"
            sx={{ marginBottom: "15px" }}
          >
            Geography Based Traffic
          </Typography>
          <Box height="200px">
            <GeographyChart isDashboard={true} />
          </Box>
        </Box> */}
      </Box>
    </Box>
  );
};

export default Prediction;
