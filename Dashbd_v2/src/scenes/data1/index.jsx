import { Box, Toolbar, Typography, useTheme } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataData1} from "../../data/mockData";
import Header from "../../components/Header";

const Data1 = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const columns = [
    { field: "id", headerName: "Cycle" },
    {
      field: "capacity",
      headerName: "Capacity",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "SoH",
      headerName: "SoH",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "resistance",
      headerName: "Resistance",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "CCCT",
      headerName: "CCCT",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "CVCT",
      headerName: "CVCT",
      flex: 1,
      cellClassName: "name-column--cell",
    },
  ];

  return (
    <Box m="20px">
      <Header title="CALCE" subtitle="CS2_35 Sample dataset" />
      <Box
        m="40px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
          "& .MuiDataGrid-toolbarContainer .MuiButton-text":{
            color: `${colors.grey[100]} !important`,
          }
        }}
      >
        <DataGrid rows={mockDataData1} columns={columns} components={{Toolbar: GridToolbar}} />
      </Box>
    </Box>
  );
};

export default Data1;
